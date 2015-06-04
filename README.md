#### Bonvin Lab webpage based on the Jekyll template [Minimal Mistakes](http://mmistakes.github.io/minimal-mistakes)

See a [live version of this website](http://haddocking.github.io/) hosted on GitHub.
For more information on the template and folder organization, visit the [original author's
web page](http://mmistakes.github.io/minimal-mistakes/theme-setup/).

#### Getting Started

##### Requirements & Dependencies

1. Ruby v2.0

##### Installation Instructions

1. Install Bundler

```bash
    $ gem install bundler
```

2. Run Bundler from the site's directory

```bash
    $ bundle install
```

3. Adapt the settings in _config.yml accordingly

##### Running the website locally

To run the web site locally, e.g. to preview changes before pushing to the repository
issue the following command:
```bash
    $ bundle exec jekyll serve
```

##### We can now make a new post simply by typing, in the main folder of the site:
```python
    $ python _utilities/create_new_article.py 'A Random Post'
```

