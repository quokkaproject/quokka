Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

### Report Bugs

Report bugs at <https://github.com/rochacbruno/quokka_ng/issues>

If you are reporting a bug, please include:

-   Your operating system name and version.
-   Run ```pip freeze``` and paste you local versions of libraries
-   Any details about your local setup that might be helpful
    in troubleshooting.
-   Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything is
open to whoever wants to implement it.

### Implement Features

Look through the [Issues](https://github.com/rochacbruno/quokka_ng/issues) board. Anything there is open to whoever wants to implement it, if you have any doubts please leave a comment the issue asking for clarification.

### Write Documentation

QuokkaProject could always use more documentation,
whether as part of the official quokka source docs,
in docstrings, or in project documentation website, or even on the web in blog posts, articles, and such.

> To help writing documentation please go to https://github.com/quokkaproject/quokkaproject.github.io and follow instructions in README

### Submit Feedback and ask for new features

The best way to send feedback is to file an issue at
<https://github.com/rochacbruno/quokka_ng/issues>

If you are proposing a feature:

-   Explain in detail how it would work.
-   Keep the scope as narrow as possible, to make it easier
    to implement.
-   Remember that this is a volunteer-driven project, and that
    contributions are welcome :)

Get Started!
------------

Ready to contribute? Here’s how to set up Quokka CMS
for local development.

1.  Fork the [quokka](https://github.com/rochacbruno/quokka_ng) repo on GitHub.
2.  Clone your fork locally:

        $ git clone git@github.com:your_name_here/quokka_ng.git
        $ cd quokka_ng/

3.  Install your local copy into a virtualenv:

        $ make create_env
        $ . venv/bin/activate
        $ make install

4. Run Quokka:

        $ make devserver

5.  Create a branch for local development:

        $ git checkout -b name-of-your-bugfix-or-feature

    Now you can make your changes locally.

6.  When you’re done making changes, check that your changes pass flake8
    and the tests:

        $ make test

7.  Commit your changes and push your branch to GitHub:

        $ git add .
        $ git commit -m "Your detailed description of your changes."
        $ git push origin name-of-your-bugfix-or-feature

8.  Submit a pull request through the GitHub website or github CLI.
