# mdbook HADDOCK tutorials

- [Usage of `mdbook`](#mdbook-usage) 
- [Use shared files](#use-shared-files)

## Use shared files

`mdbook` only works with relative paths, which is not easy when we want to point a file outside of it.
The solution found was to create a link to the file in the `src` of the newly created tutorial book directory.

For this run:
```bash
# Go to src directory of the tutorial
cd new-tutorial/src/
# Create a link to a file
ln -s ../../shared/shared/intro/haddock.md .

# Or simply link the entire directory content (including images and so..)
ln -s ../../shared/* .
```

then it can be added in the `SUMMERY.md`, which is the file used by `mdbook` to know the order of the files in the book.


## mdbook usage

### Install mdbook

`mdbook` must be installed (see [how to install mdbook](https://rust-lang.github.io/mdBook/index.html)).

### Create a new book

```bash
mdbook init new-tutorial --title "New tutorial"
```

### Build a new book

```bash
mdbook build new-tutorial
# or
/Applications/mdbook build new-tutorial
```

This will create/update the content in the `new-tutorial/book/` directory.
The book can be accessed using the file named `new-tutorial/book/index.html`, with your favourit web-browser !


