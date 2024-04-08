# Package your backend application

In order to deploy our backend, we need to build a zip file that contains our backend code
alongside its dependencies. This zip file should contain dependencies that are compatible
with `x86_64` architecture.

We do this in four steps.

1. Use poetry to export our dependencies to a requirements file. We will use the `poetry
   export` command with three flags: `-f requirements.txt` specifies the format; `--output
   {filename}` specifies the output file for the dependencies; and `--without-hashes`
   removes some unnecessary detail from the output file. You are free to choose any output
   file, however this section will assume that we exported to `requirements.txt`.
   ```bash
    poetry export \
    -f requirements.txt \
    --output requirements.txt \
    --without-hashes
    ```

2. Use pip to install the dependencies. We will use the `pip install` command with four
   flags: `-r requirements.txt` defines where the requirements can be located; `-t
   {directory}` specifies the directory where the dependencies will be installed;
   `--platform manylinux2014_x86_64` indicates that dependencies should be installed for
   the `x86_64` architecture; and `--only-binary=:all:` indicates that only binary
   packages should be installed. You are free to deploy to any directory, however this
   document will assume that we installed to the `build` directory.
   ```bash
   python -m pip install \
   -r requirements.txt \
   -t build \
   --platform manylinux2014_x86_64 \
   --only-binary=:all:
   ```

3. Compress the dependencies into a zip file. We will use the flags `-r` to indicate
   recursive zipping and `-9` to indicate maximum compression. You are free to compress to
   any zip file, however this section will assume that we compressed to `build.zip`,
   located next to the `build` directory.
   ```bash
   cd build
   zip -r9 ../build.zip ./
   cd ..
   ```

4. Add the backend code to the zip file. You may optionally remove all of the
   `__pycache__` folders for a slightly smaller footprint. We will use the `-r` flag to
   indicate recursive zippping and the `-u` flag to indicate update only changed files.
   ```bash
   zip -ur build.zip ./backend
   ```

The only artifact we need is the zip file `build.zip`, so you are free to cleanup extra
files, for example the `build` directory.

Anytime a new dependency is added to your application, these 4 steps would need to be
repeated. And anytime your backend code is updated, the fourth step would need to be
repeated.

