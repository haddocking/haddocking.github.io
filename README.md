# Bonvin Lab webpage based on the Jekyll template [Minimal Mistakes](http://mmistakes.github.io/minimal-mistakes)

See a [live version of this website](http://haddocking.github.io/) hosted on GitHub.
For more information on the template and folder organization, visit the [original author's
web page](http://mmistakes.github.io/minimal-mistakes/theme-setup/).

## Getting Started

To ensure whatever you create/change appears as faithfully as possible after pushing to the main repository, install the version of Ruby and the gems used by Github. See a list [here](https://pages.github.com/versions/).

### Installation Instructions (updt. Nov. 2023)

Following the instructions from: https://github.com/BillRaymond/install-jekyll-apple-silicon/blob/main/README.md

And using homebrew


1. Install ruby3.0

```
brew install ruby@3.0
```

2. Add path to ruby3.0 in .bashrc (or .bash_provile)

export PATH="/opt/homebrew/opt/ruby@3.0/bin/:$PATH"

3. Restart your terminal and make sure you are now using ruby3.0

```
ruby -v
```

4. Install Jekyll and Bundler

```
gem install --user-install bundler jekyll
```

5. Add the path to the gems to in .bashrc (or .bash_provile)

export PATH="~/.local/share/gem/ruby/3.0.0/bin:$PATH"


6. Clone the haddocking.github.io repository and install all dependency Gems with Bundler

```bash
git clone https://github.com/haddocking/haddocking.github.io.git haddocking-website
cd haddocking-website
bundle init
bundle add jekyll --version "~>4.2"
bundle config set --local path 'vendor/bundle'
bundle install
bundle exec jekyll new --force --skip-bundle .
bundle add webrick
bundle install
bundle update
```

7. Adapt the settings in _config.yml accordingly
In order for links to properly work, the `url` setting in must be set accordingly, otherwise you will be redirected to the live version. This sets all the `site.url` variable calls throughout _layouts/,  _includes/, etc.

```yaml
url: "" # Empty string will render the page successfully locally. Do not commit it to the main repository!
incremental: true # This will be disabled by Github, but is useful for testing changes locally!
```

### Running the website locally

To preview changes, which you should always do before committing anything or making any pull requests, run the web server locally using the following:

```bash --login
    $ bundle exec jekyll serve
```

### Small utility to create a new post automatically. Quick and dirty replacement of `octopress new post`

```python
    $ python _utilities/create_new_article.py 'A Random Post'
```

8. For updating jeckyll and bundle

```bash
    $ gem update jekyll
    $ gem update bundle 
