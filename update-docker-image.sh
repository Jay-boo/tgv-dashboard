docker build . -t tgv

# S'authentifier avec gcloud
gcloud auth configure-docker europe-west1-docker.pkg.dev

# tag l'image qui a été build précédemment
docker tag tgv europe-west1-docker.pkg.dev/ensai-2023-373710/ja-depot/tgv

# push le tag
docker push europe-west1-docker.pkg.dev/ensai-2023-373710/ja-depot/tgv

