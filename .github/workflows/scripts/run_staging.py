import sys
import asyncio
import os
import pathlib
import yaml
import itertools

from binderbot.binderbot import BinderUser


BINDER_URLS = {
    "https://binder.pangeo.io": "https://staging.binder.pangeo.io",
    "https://aws-uswest2-binder.pangeo.io": "https://staging.aws-uswest2-binder.pangeo.io/",
}
NB_TIMEOUT = 1200  # This is ~2X the longest cell (storage benchmarks)


async def main():
    files = list(pathlib.Path("pangeo-gallery").glob("**/binder-gallery.yaml"))
    root = pathlib.Path("pangeo-gallery").absolute()

    configs = {}
    for file in files:
        with open(file) as f:
            configs[file] = yaml.safe_load(f)

    def key(x):
        return x[1]["binder_url"], x[1]["binder_repo"], x[1]["binder_ref"]

    # Grouping by binder let's us cut down on the number of image builds / pod startups.
    configs = dict(sorted(configs.items(), key=key))
    groups = itertools.groupby(configs.items(), key=key)

    exceptions = {}

    for (binder_url, binder_repo, binder_ref), group in groups:
        if binder_repo == "pangeo-gallery/default-binder":
            binder_ref = "staging"
        binder_url = BINDER_URLS.get(binder_url)
        # TODO: switch for not skipping if not in staging.
        if not binder_url:
            print(f"Skipping for {binder_url}, {binder_repo}, {binder_url}")
            continue

        print(f"Staring BinderUser for {binder_url}, {binder_repo}, {binder_url}")
        async with BinderUser(binder_url, binder_repo, binder_ref) as jovyan:
            for file, config in group:
                try:
                    os.chdir(file.parent.absolute())
                    notebooks = [str(x) for x in (pathlib.Path(".").glob("*.ipynb"))]

                    print(
                        f"running {file} on {binder_url} with {binder_repo}@{binder_ref}"
                    )
                    try:
                        await jovyan.run(
                            notebooks, download=False, nb_timeout=NB_TIMEOUT
                        )
                    except Exception as e:
                        exceptions[file] = e
                        print("exception in", file)
                finally:
                    os.chdir(root)

            await jovyan.stop_kernel()

    if exceptions:
        print(exceptions)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
