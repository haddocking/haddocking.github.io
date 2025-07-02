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
git clone --depth 1 https://github.com/haddocking/haddocking.github.io.git haddocking-website
cd bonvinlab-website
```

#### Install website dependencies

These are Ruby packages (gems) required to run the website.
First install Ruby's dependency manager `bundler` and `jekyll`

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

Go ahead and edit/add what you need, to see the rendered version, refresh the page.
