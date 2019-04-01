# Blockchain Docs

Docsite for [github.com/target/ConsenSource](https://github.com/target/ConsenSource)

## How to contribute to this page?

1. Clone this repo.
2. Install gutenberg.
```
brew install gutenberg
```
3. Make your changes in the `/docs_content` directory.
4. Build the site from the `/docs_content` directory, but output it to the `/docs` directory.
```
$ pwd
~/path/to/repo/docs_content
$ gutenberg build --output-dir ../docs
```
5. Commit your changes and create a PR.
6. Once changes are merged, the new content will be published at https://pages.github.com/target/ConsenSource/about .
