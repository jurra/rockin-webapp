Dont build in docker-compose
Build and store your images in a registry and pull them from there.

docker build
docker-compose build

open shift?
kubernetes?

Where is code?
Where is your package build?
Where do you run it?


Use the harbor platform for images

We could use travis ci for builds
CVEs

# Push to a registry that does security
1. registry.ict.tudelft.nl
2. registry.tudelft.nl (Open to the world), be careful. OIDC provider needs to be used the sso of the TU Delft.
(This is for CI CD in the correct way)



## How tos
Goal push container to the registry
Then pull it from the registry into the production server
Mostly relevant to maintain images versions and to have a central place to store them
Management of images basically....
Avoid build in the server as well

- docker login from my machine to the cli


# Linters and smells

# Packaging, distribution and deployment of the application