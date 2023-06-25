from setuptools import setup
from git import Repo
import os.path

# Clone data model from pydantic as a submodule
if not os.path.exists("datamodel"):
    repo_url = "git@github.com:jurra/rockin-datamodel.git"
    Repo.clone_from(repo_url, "datamodel")
#     repo = Repo("rockin-datamodel")
#     os.rename("rockin-datamodel", "pydantic_models")

setup(name='rockin',
      version='0.1',
      packages=['rockin'],
      )
