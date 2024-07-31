# of-scraper-post

## What is this?

This is a script to run after each performer processed by [OF-Scraper](https://github.com/datawhores/OF-Scraper).

## How to use

>[!NOTE]\
> These steps work on macOS or Linux, they do not work on Windows

1) Make sure that the `script.sh` matches where the files are, and if you are using a [venv](https://docs.python.org/3/library/venv.html) or not.
2) Either edit your OFscraper config file `.config/ofscraper/config.json` or add additional argument to your OFscraper script run
    * in the `advanced_options` section of the config file, add a record for `post_download_script` which points to the `script.sh`

    ~~~JSON
        {
            "advanced_options": {
                "post_download_script": "/path/to/your/git/clone/of-scraper-post/script.sh",
            }
        }
    ~~~

    * add the `-ds` or `--download-script` argument
        * more details in the [OF-Scraper gitbook](https://of-scraper.gitbook.io/of-scraper/command-reference/shared-options/common-option-groups/advanced-args#ds-download-script-argument)
