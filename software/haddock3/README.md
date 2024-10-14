# Compile the book

This manual is ment to be compiled by `mdbook`.

To generate it, mdbook must be installed (see [how to install mdbook](https://rust-lang.github.io/mdBook/index.html)).


Then run the following command, once in the `software/haddock3/` directory:

```bash
mdbook build haddock3-manual --dest-dir ../manual
# or
/Applications/mdbook build haddock3-manual --dest-dir ../manual
```
