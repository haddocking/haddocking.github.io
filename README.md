# BonvinLab webpage

> Go to [bonvinlab.org](https://bonvinlab.org) for
> the latest version of the BonvinLab website.

## Adding to the page

### Install dependencies

#### Ruby

Install Ruby following your system's instructions.

```text
brew install ruby
```

```text
sudo apt install ruby-full
```

```text
sudo pacman -S ruby ruby-erb
```

#### Clone this repository

```bash
git clone --depth 1 https://github.com/haddocking/haddocking.github.io.git bonvinlab-website
cd bonvinlab-website
```

#### Install website dependencies

These are Ruby packages (gems) required to run the website.
First, install Ruby's dependency manager `bundler` and `jekyll`

```bash
# Change the ruby version if you are not using `3.4.0`
export PATH="$HOME/.local/share/gem/ruby/3.4.0/bin:$PATH"
gem install --user-install bundler jekyll
```

Now install the required website dependencies (gems) using Bundler.

```bash
bundle config set --local path 'vendor/bundle'
bundle install
bundle update
```

### Running the site locally

Serve it locally by running:

```bash
bundle exec jekyll serve
```

It should now be served on [http://127.0.0.1:4000](http://127.0.0.1:4000)

Go ahead and edit/add what you need! To see the rendered version, refresh the page.

## Styling

The site's CSS is compiled by Jekyll from the Sass sources in `_sass/`, with
`assets/css/main.scss` as the entry point. Editing a file under `_sass/` is all
that is needed — `assets/css/main.css` is regenerated on every build and is what
`_includes/_head.html` loads.

There is no manual regeneration step. The site previously shipped a committed,
hand-optimised `assets/css/main_pretty.css`; nothing in the repo regenerated it,
so it had drifted from the Sass sources and some styles never reached the site.
It has been removed — do not reintroduce a committed CSS artifact.

Source maps are disabled for the build (`sourcemap: never` in `_config.yml`). Set
it to `always` temporarily if you need to trace a rule back to its partial.
