group "default" {
    targets = ["of-scraper-post"]
}

target "alpine" {
    dockerfile = "../OF-Scraper/Dockerfile.alpine"
    context = "../OF-Scraper"
    platforms = ["linux/amd64", "linux/arm64"]
    args = {
        PYTHON_VERSION = "3.12",
        SIZE = "full"
        }
}

target "of-scraper-post" {
    contexts = {
        "of-scraper" = "target:alpine"
    }
    dockerfile = "Dockerfile"
    platforms = ["linux/amd64", "linux/arm64"]
    tags = [
        "024848464090.dkr.ecr.us-east-2.amazonaws.com/of-scraper:full",
        "024848464090.dkr.ecr.us-east-2.amazonaws.com/of-scraper:latest"
    ]
}
