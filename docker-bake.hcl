group "default" {
    targets = ["of-scraper-post", "of-scraper_python-3-12-alpine-full", "of-scraper_python-3-12-alpine-minimal", "of-scraper_python-3-11-alpine-full", "of-scraper_python-3-11-alpine-minimal", "of-scraper_full", "of-scraper_minimal"]
}

target "of-scraper_python-3-12-alpine-full" {
    dockerfile = "../OF-Scraper/Dockerfile.3.12-alpine-full"
    context = "../OF-Scraper"
    platforms = ["linux/amd64", "linux/arm64"]
    tags = ["of-scraper:3.11.6-python-3.12-alpine-full"]
}
target "of-scraper_python-3-12-alpine-minimal" {
    dockerfile = "../OF-Scraper/Dockerfile.3.12-alpine-minimal"
    context = "../OF-Scraper"
    platforms = ["linux/amd64", "linux/arm64"]
    tags = ["of-scraper:3.11.6-python-3.12-alpine-minimal"]
}
target "of-scraper_python-3-11-alpine-full" {
    dockerfile = "../OF-Scraper/Dockerfile.3.11-alpine-full"
    context = "../OF-Scraper"
    platforms = ["linux/amd64", "linux/arm64"]
    tags = ["of-scraper:3.11.6-python-3.11-alpine-full"]
}
target "of-scraper_python-3-11-alpine-minimal" {
    dockerfile = "../OF-Scraper/Dockerfile.3.11-alpine-minimal"
    context = "../OF-Scraper"
    platforms = ["linux/amd64", "linux/arm64"]
    tags = ["of-scraper:3.11.6-python-3.11-alpine-minimal"]
}
target "of-scraper_full" {
    dockerfile = "../OF-Scraper/Dockerfile.full"
    context = "../OF-Scraper"
    platforms = ["linux/amd64", "linux/arm64"]
    tags = ["of-scraper:3.11.6-full", "of-scraper:latest-full", "of-scraper:3.11-full", "of-scraper:3-full"]
}
target "of-scraper_minimal" {
    dockerfile = "../OF-Scraper/Dockerfile.minimal"
    context = "../OF-Scraper"
    platforms = ["linux/amd64", "linux/arm64"]
    tags = ["of-scraper:3.11.6-minimal", "of-scraper:latest-minimal", "of-scraper:3.11-minimal", "of-scraper:3-minimal", "of-scraper:3.11.6", "of-scraper:latest", "of-scraper:3.11", "of-scraper:3"]
}

target "of-scraper-post" {
    contexts = {
        "of-scraper" = "target:of-scraper_python-3-12-alpine-full"
    }
    dockerfile = "Dockerfile"
    platforms = ["linux/amd64", "linux/arm64"]
    tags = ["024848464090.dkr.ecr.us-east-2.amazonaws.com/of-scraper:latest-full",
            "024848464090.dkr.ecr.us-east-2.amazonaws.com/of-scraper:3.11.6-full",
            "024848464090.dkr.ecr.us-east-2.amazonaws.com/of-scraper:3.11-full",
            "024848464090.dkr.ecr.us-east-2.amazonaws.com/of-scraper:3-full",
            "024848464090.dkr.ecr.us-east-2.amazonaws.com/of-scraper:latest"]
}
