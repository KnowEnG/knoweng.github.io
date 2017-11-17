# knoweng.github.io


Quick Start:
  * edit `repos.metadata.yml` if necessary
  * `./gen_index_page.py`
  * verify `out.md` is acceptable
  * `mv out.md index.md`
  * commit/push the changed files (`index.md`, maybe `repos.metadata.yml`) back to the repo


Use `gen_index_page.py` to create an index page for the repos.

You can likely just use this script as follows:

```
./gen_index_page.py
```

This will get the repos info from the GitHub API URL.
The default repos metadata file (`-rmf`) is `repos.metadata.yml`.
The default output file (`-of`) is `out.md`.

If you have a previously saved repos info file and want to avoid
connecting to GitHub to get that, you can use:

```
./gen_index_page.py -rif repositories?q=user:KnowEnG
```

or

```
./gen_index_page.py -rif repos.info.json
```

If you want to save the repos info to a file (`repos.info.json`) when
you get it, use:

```
./gen_index_page.py -s
```

If you want to specify the repos metadata file, use:

```
./gen_index_page.py -rmf repos.metadata.yml
```

If you want to specify the output file, use:

```
./gen_index_page.py -of out.md
```

Most likely you will want to place the output in `index.md`.  To do
that, you can either do the following command after you run the
script:

```
mv out.md index.md
```

or specify `index.md` as the output file:

```
./gen_index_page.py -of index.md
```

Just make sure you're not overwriting a file that you want to save.


To get the repos info from the GitHub API URL for an entire
user/organization, use:

```
wget --header='Accept: application/vnd.github.mercy-preview+json' 'https://api.github.com/search/repositories?q=user:KnowEnG'
```

For a specific repo, use:

```
wget --header='Accept: application/vnd.github.mercy-preview+json' 'https://api.github.com/search/repositories?q=user:KnowEnG+KnowEnG_CWL'
```

