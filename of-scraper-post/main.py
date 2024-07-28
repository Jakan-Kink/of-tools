import asyncio
import json
import logging
import os
import sys
import time

# from datetime import date, datetime, timedelta, timezone
from functools import reduce
from pprint import PrettyPrinter, pformat
from string import Formatter
from typing import Any
from urllib.parse import urlparse

import yaml  # type: ignore[unused-ignore]
from numpy.random import default_rng
from stashapi.stashapp import StashInterface

logger = logging.getLogger(__name__)
FORMAT = (
    "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s-%(lineno)d - %(message)s"
)
LOG_FILE = "/Users/jakan/Development/of-scraper-post/debug.log"
file_logger = logging.getLogger("file_logger")
logging.addLevelName(5, "TRACE")
file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
file_handler.setFormatter(logging.Formatter(FORMAT))
file_logger.addHandler(file_handler)
file_logger.setLevel(logging.DEBUG)
file_logger.propagate = False
runtime_settings = {}
args = []
semaphore = asyncio.Semaphore(16)
rng = default_rng()


class Default(dict[Any, Any]):
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


pprint = PrettyPrinter(
    indent=4, depth=2, compact=True, width=(os.get_terminal_size().columns - 5)
).pprint


def load_config(config_file: str) -> None:
    global runtime_settings
    _, ext = os.path.splitext(config_file)
    with open(config_file) as file:
        if ext.lower() == ".json":
            data = json.load(file)
        elif ext.lower() == ".yaml" or ext.lower() == ".yml":
            data = yaml.safe_load(file)
        else:
            raise ValueError(
                f"Unsupported file extension {ext}. Please use .json or .yaml/.yml"
            )
    runtime_settings = data
    runtime_settings["config_file"] = config_file


# Stolen from https://stackoverflow.com/a/46890853 with some added type casting
def deep_get(
    dictionary: dict, keys: str, default: type[ValueError] | None = None
) -> Any:
    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
        keys.split("."),
        dictionary,
    )


def format_directory(dir_type: str | None = None, **vars) -> str:
    global runtime_settings
    return_string: str = ""
    if dir_type is None:
        raise ValueError("dir_type is required")
    if dir_type not in [
        "stash_location",
        "dir_format_stash",
    ]:
        raise ValueError(f"Unsupported dir_type: {dir_type}")
    path_key = (
        f"of_scraper.folders.{dir_type}"
        if dir_type != "dir_format_stash"
        else "of_scraper.folders.dir_format"
    )
    try:
        return_string = deep_get(runtime_settings, path_key, ValueError)
    except ValueError as e:
        file_logger.warning(f"Error: {e}")
        exit(1)
    if "metadata_format" in dir_type or "dir_format" in dir_type:
        save_or_stash = (
            "save_location"
            if "metadata_format" in dir_type or "dir_format" == dir_type
            else "stash_location"
        )
        return_string = return_string.format_map(
            Default(dict(**vars, save_location=format_directory(save_or_stash)))
        )
    fieldnames = [fname for _, fname, _, _ in Formatter().parse(return_string) if fname]
    replacements = {fname: vars.get("missing_values", "**") for fname in fieldnames}
    return_string = return_string.format_map(Default(dict(**replacements)))
    return return_string


async def generate_metadata_for_scene(stash: StashInterface, scene_id: int) -> None:
    stash.metadata_generate(
        {
            "covers": True,
            "sprites": True,
            "previews": True,
            "imagePreviews": True,
            "previewOptions": {
                "previewSegments": 12,
                "previewSegmentDuration": 0.75,
                "previewExcludeStart": "0",
                "previewExcludeEnd": "0",
                "previewPreset": "slow",
            },
            "markers": True,
            "markerImagePreviews": True,
            "markerScreenshots": True,
            "transcodes": False,
            "phashes": True,
            "interactiveHeatmapsSpeeds": True,
            "imageThumbnails": True,
            "clipPreviews": True,
            "sceneIDs": [scene_id],
            "overwrite": False,
        }
    )


def main() -> None:
    global runtime_settings
    global args
    args = sys.argv[1:]
    # for index, arg in enumerate(args):
    #     file_logger.info(pformat(f"Arg-{index} passed: {arg}"))
    load_config("/Users/jakan/Development/of-scraper-post/config.yml")
    username = args[0]
    user_id = args[1]
    file_logger.info(f"Username: {username}")
    file_logger.info(f"User ID: {user_id}")
    stash = StashInterface(
        {
            "scheme": runtime_settings["stashapp"]["scheme"],
            "host": runtime_settings["stashapp"]["host"],
            "port": runtime_settings["stashapp"]["port"],
            "ApiKey": runtime_settings["stashapp"]["api_key"],
        }
    )
    path = [format_directory("dir_format_stash", model_username=username)]
    file_logger.info(f"path: {path}")
    job = stash.metadata_scan(paths=path)
    running_job = True
    paid_content = json.loads(args[2])
    # file_logger.info(pformat(f"Paind Content type: {type(paid_content)} - {paid_content}"))
    posted_content = json.loads(args[3])
    # file_logger.info(pformat(f"Posted Content type: {type(posted_content)} - {posted_content}"))
    contents = paid_content + posted_content
    file_logger.info(f"Content Length: {len(contents)}")
    start_time = time.time()
    prior_status: str = ""
    while running_job:
        job_status = stash.find_job(job)
        if job_status["status"] in ["FINISHED", "FAILED", "CANCELLED"]:
            running_job = False
            break
        if ((time.time() - start_time) > 120) and job_status["status"] not in [
            "RUNNING",
            "STOPPING",
        ]:
            file_logger.info("Timeout: 120 seconds and still waiting to start")
            break
        else:
            if prior_status == job_status["status"] and job_status["status"] == "READY":
                time.sleep(0.5)
                continue
            try:
                file_logger.info(
                    f"Job status: {job_status['status']} - {job_status['description']} - Sub-Task: {job_status['subTasks']}"
                )
            except KeyError:
                file_logger.info(
                    f"Job status: {job_status['status']} - {job_status['description']}"
                )
            except TypeError:
                file_logger.info(
                    f"Job status: {job_status['status']} - {job_status['description']}"
                )
            prior_status = job_status["status"]
            time.sleep(0.5)
    file_logger.info("Beginning of media looping")
    for content in contents:
        if (
            content.get("responseType", None) == "profile"
            or content.get("responsetype", None) == "profile"
        ):
            file_logger.info("Profile")
            continue
        # file_logger.info(pformat(f"Content: {content}"))
        if content.get("canPurchase", False):
            file_logger.info(
                "Message content still available for purchase - skipping\n\n"
            )
            continue
        if content.get("price", 0) > 0 and content.get("canViewMedia", False):
            file_logger.info("Content is paid and can be viewed")
        file_logger.info(f"Media Count: {content.get('mediaCount', 0)}")
        file_logger.info(f"Media Length: {len(content.get('media', []))}")
        for media in content.get("media", []):
            if media.get("type", None) == "video":
                filename: str = ""
                file_logger.info("Video")
                if media.get("canView", False):
                    file_logger.info("Video can be viewed")
                else:
                    file_logger.info("Video cannot be viewed")
                    continue
                if media.get("source", None) is not None:
                    if media["source"].get("source", None) is not None:
                        source_url = urlparse(media["source"]["source"])
                        source_path = source_url.path
                        file_logger.info(pformat(f"Source: {source_path}"))
                        source_array = source_path.split("/")
                        source_filename = source_array[-1]
                        file_logger.info(pformat(f"Filename: {source_filename}"))
                        filename = source_filename
                    else:
                        file_logger.info("No source available")
                if media.get("files", None) is not None and filename == "":
                    file = media.get("files", {})
                    file_logger.info(pformat(f"File: {file}"))
                    if file.get("drm", False):
                        file_logger.info("File is DRM protected")
                        if file["drm"].get("manifest", None) is not None:
                            file_logger.info(
                                pformat(f"Manifest: {file['drm']['manifest']}")
                            )
                            hls = file["drm"]["manifest"].get("hls", None)
                            if hls is not None:
                                hls_url = urlparse(hls)
                                hls_path = hls_url.path
                                file_logger.info(pformat(f"HLS: {hls_path}"))
                                hls_array = hls_path.split("/")
                                hls_filename = hls_array[-1]
                                file_logger.info(pformat(f"Filename: {hls_filename}"))
                                filename = hls_filename
                            dash = file["drm"]["manifest"].get("dash", None)
                            if dash is not None:
                                dash_url = urlparse(dash)
                                dash_path = dash_url.path
                                file_logger.info(pformat(f"DASH: {dash_path}"))
                                dash_array = dash_path.split("/")
                                dash_filename = dash_array[-1]
                                file_logger.info(pformat(f"Filename: {dash_filename}"))
                filename = os.path.splitext(filename)[0]
                file_logger.info(pformat(f"Query File basename: {filename}"))
                scenes = stash.find_scenes(filter={"per_page": -1}, q=filename)
                if scenes is not None:
                    file_logger.info(pformat(f"Scenes: {len(scenes)}"))
                    for scene in scenes:
                        asyncio.run(generate_metadata_for_scene(stash, scene["id"]))
            elif media.get("type", None) == "photo":
                file_logger.info("Photo")
                if media.get("canView", False):
                    file_logger.info("Image can be viewed")
                else:
                    continue
                if media.get("source", None) is not None:
                    if media["source"].get("source", None) is not None:
                        file_logger.info(
                            pformat(f"Source: {urlparse(media['source']['source'])}")
                        )
                        continue
                    else:
                        file_logger.info("No source image available")
                if media.get("files", None) is not None:
                    for file in media["files"]:
                        file_logger.info(pformat(f"File: {file}"))
            else:
                file_logger.info(f"Unknown media type - {media.get('type', None)}")
                continue
            # file_logger.info(pformat(f"Media: {media}"))
        file_logger.info("End of Content\n\n\n")
    file_logger.info(f"End of user {username}")
    file_logger.info("End of main\n\n\n\n\n")


if __name__ == "__main__":
    main()
