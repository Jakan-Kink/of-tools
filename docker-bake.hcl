group "default" {
    targets = ["of-scraper-post", "of-scraper"]
}

target "of-scraper" {
    dockerfile = "../OF-Scraper/Dockerfile"
    context = "../OF-Scraper"
    platforms = ["linux/amd64", "linux/arm64"]
}

target "of-scraper-post" {
    contexts = {
        "of-scraper" = "target:of-scraper"
    }
    dockerfile = "Dockerfile"
    platforms = ["linux/amd64", "linux/arm64"]
}
