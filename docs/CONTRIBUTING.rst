========================
Contributing to manga-py
========================

Thanks for your interests in manga-py!
Your interaction will benefit others who use this project.
manga-py welcomes contributions of many forms.

Examples of contributions include:

- Coding
- Documenting
- Reporting bugs
- Suggesting
- Questioning
- Sponsoring

This contribution guidelines are available in the repository at
``./docs/CONTRIBUTING.rst``, or online at `GitHub repository`_.

Interested in contribute?
Read on!

Code of Conduct
===============

As a contributor, you can help us keep the manga-py community open and inclusive.
Please read and follow manga-py's `Code of Conduct`_.
Here are things we expect from you, and you will expect from everybody:

- Be kind, because people comes from different backgrounds.
- When contributing to manga-py, you agree with `Code of Conduct`_ terms.

Follow the sections below to know the step-by-step for your specific contributions case.

Coding, Documenting
===================

Before submitting a new issue, do a search (at `GitHub Issues`_ and `GitHub Pull Requests`_) to see if your desired issue was already debated.
New source-codes and patches can be submitted as `GitHub Pull Requests`_.
Choose the specific pull-request template to submit your source-code.

Tips for new contributors
-------------------------

Starting in a existing project can intimidate and frustate too.
To minimize that:

- Pick a area that you care about.
- You don't need to be an expert on the area you have interest.
- Analyze the git/file history to understand how it evolved.
- Start small.
- Ask first, mainly about big tasks.
- Give a feedback, wait for feedback, respond to feedback.
- Make explicit your thoughts (e.g. I dont know if it is complete, if it is helpful, if it is testable...).
- Be rigorous (about doc, `PEP8`_, tests...).

Some steps from-easy-to-hard way to get involved with manga-py development:

1. Reproduce bugs.
    - Read a bug issue on `GitHub Issues`_ and try to reproduce it.
    - Make a note about what was outputted, if you can or can not reproduce it.
    - `Write Tests`_ to the bug's behavior.
    - Consider writing a patch to fix it, if you fell motivated to do that.

2. Read closed issues on `GitHub Issues`_.
    - Familiarize with the codebase and the process.
    - Look at the commits, specially: the commit message and, git additions and deletions.
    - Review the code: Matches `PEP8`_? Needs (better) documentation? Needs (more) tests?
    - Flag/tag the issue more accurately.

3. Update old patches.
    - Remove unnecessary code.
    - Deprecate a feature.
    - Rewrite ambiguous terms (e.g namespaces, methods etc).
    - Retype all new input table parameters for test cases.
    - Verify if regex strings matches yet the providers URLs.

4. `Writing Documentation`_.

Submit a pull request
----------------------

Before you submit a pull request (PR), do:

1. Verify that your `GitHub Pull Requests`_ is not duplicated.

2. Prepare your repository, by:

    2.1. Do your changes in a separate branch.
        - Branches MUST have descriptive names starting with prefixes:
            - *ref*actor, *lin*t, *doc*ument, *fix* bug, *enh*ance, add *sit*e, add *fea*ture, *oth*er.
            - Good examples of names for branches: `fix/signin-issue` or `fea/issue-templates`.

    2.2. Write a descriptive commit message with a short title (first line) and imperative mode.
        - E.g.: `[fix] resolve the second bug`.

    2.3. Submit only one commit per pull request.
        - `squash commits`_ by rebasing to split/join them.

    2.4. `Testing`_ your changes and pass on all of them.
        - If did not passed, fix them and amend your commit (`git commit --amend`).

Now, open your pull request:

1. Target your pull request to the `master` branch on this repository.

2. Give a descriptive title to your pull request.
    - E.g.: `[fix] resolve the second bug`.

3. Use the `pull request template`_ to structurize the description of your changes.

4. Comment your pull request with `closes #XXXX` to auto-close the issue that your pull request fixes.

Add support for a new site
--------------------------

To add a new site onto manga-py, follow these steps:

1. `Set up Developer's environment`_.

2. Update your local manga-py repository from upstream (i.e. official) repository:

.. code:: bash

    (my_env) $ git fetch upstream
    remote: Enumerating objects: 26, done.
    remote: Counting objects: 100% (26/26), done.
    remote: Compressing objects: 100% (23/23), done.
    remote: Total 26 (delta 1), reused 21 (delta 1), pack-reused 0
    Unpacking objects: 100% (26/26), done.
    From https://github.com/manga-py/manga-py
       9b15846..468720b  2.x        -> upstream/2.x

3. Start a new git branch:

.. code:: bash

    (my_env) $ git checkout -b yourprovider_com
    (my_env) $ git rebase stable_1.x

4. Code your extractor at:

.. code:: bash

    (my_env) $ touch manga_py/providers/yourprovider_com.py

Have a look at ``./manga_py/providers/`` to see some providers already done.
You can get insides about methods and classes to be implemented by them.
And `write tests`_ to your new code.

5. Add your new site onto ``providers_list`` dictionary at ``manga_py/providers/__init__.py`` file. E.g:

.. code:: python

    ...

    providers_list = {
        'yourprovider_com': [
            r'yourprovider\.com/manga/.',
        ],

    ...

6. `Testing`_, and get a OK by passing all tests.

7. Now with Git, `add, commit and push`_ your new/modified files to *your* remote repository.

8. Make a `pull request`_ to manga-py (upstream/official) repository from *your* remote repository.

Done!
Your new site was added to manga-py!

Set up Developer's environment
------------------------------

This project is developed with `Python`_ programming language, and tracked by `GitHub`_.
So to code, we recommend preparing a Python environment.
Follow the steps:

1. Firstly, `install Python`_, `install Git`_ and, `sign in GitHub`_.

2. Create a *clean (new)* virtual environment:

.. code:: bash

    $ python3 -m venv my_env
    $ ls
    my_env

3. Activate your virtual environment:

.. code:: bash

    $ source my_env/bin/activate
    (my_env) $

When you conclude all development (i.e. closing terminal), deactivate your virtual environment:

.. code:: bash

    (my_env) $ deactivate
    $

4. Clone manga-py repository:

.. code:: bash

    (my_env) $ git clone https://github.com/YOUR_GITHUB_NICKNAME/manga-py.git
    Cloning into 'manga-py'...
    remote: Enumerating objects: 60, done.
    remote: Counting objects: 100% (60/60), done.
    remote: Compressing objects: 100% (45/45), done.
    remote: Total 10917 (delta 21), reused 34 (delta 14), pack-reused 10857
    Receiving objects: 100% (10917/10917), 23.82 MiB | 576.00 KiB/s, done.
    Resolving deltas: 100% (8487/8487), done.

5. Install manga-py's ``./requirements_dev.txt`` under your virtual environment:

.. code:: bash

    (my_env) $ ls ./manga-py/ && pip install -r ./requirements_dev.txt
    Collecting lxml (from -r ./requirements.txt (line 1))
    ...(outputted lines omitted for readability)

That's all to start your contribution by source-code development.

Testing
-------

Ensure that your contribution passes all tests.
If there are test failures, address them to pass all tests.
This is necessary before we can merge your contribution.

So, before running manga-py tests, `Set up Developer's environment`_.
Once you have that set up, run ``python3 ./run_tests.py``:

.. code:: bash

    (my_env) $ python3 ./run_tests.py
    python3 ./run_tests.py
    ..................................................
    ----------------------------------------------------------------------
    Ran 50 tests in 52.691s
    
    OK

And this result shows that the manga-py passes gracefully from its tests.

Write Tests
+++++++++++

.. TODO

Style Guide
-----------

manga-py is developed using Python, documented with RST and, backed up at GitHub.
So, its style uses:

- `PEP8`_: Style Guide for Python Code, so apply it for Python source-code and docstrings.
- `reStructuredText`_: all markup for RST files.
- `GitHub Flavored Markdow`_: for all text written at `GitHub Issues`_ and `GitHub Pull Requests`_ track systems.
    - E.g.: use `mentions`_ and `issue/pull-request references`_ to address your contribution more properly.

To get your one ``*.py`` under `PEP8`_ format fastly, run `yapf`_: ``$ yapf ./your_file.py``
And to validate your one ``*.py`` under `PEP8`_ style, run `pylint`_: ``$ pylint ./your_file.py``


Writing Documentation
+++++++++++++++++++++

Documentation is important.
By it, a new comer can understand what the project does and how to use it.
Most of the raw documentation stay at ``./`` and ``./docs`` folders.

Documentation changes in two forms:

- General improvements: typo corrections, error fixes, clearer writing, adding examples.
- New features: explaining added (newly) features.

Specifically, manga-py have these kinds of documentations:
- `Docstrings`_: it is a Python built in, where a string explains a implementation (e.g. module, method, class...).
- `reStructuredText`_: used to explain the project in a general way.

To improve the documentation, try:

- Short sentences is better than long sentences.
- Avoid complicated words.
- Exemplify.
- Run a spelling checker.
- Fix `*.rst` and `*.md` markup and broken links/urls.
- Get good inspirations from others projects repositories.

Reporting bugs, Suggesting, Questioning
=======================================

manga-py uses `GitHub Issues`_.
It keeps track of bugs, feature requests, suggestions and questions.
Start by searching through the `GitHub Issues`_ and `GitHub Pull Requests`_.
Maybe someone else has raised a similar idea or question.
Anybody is welcome to join these conversations.
If you don't see your idea listed, so please choose the specific issue template to submit your idea.
When preparing your issue body, specially reporting bugs:

- Include the full output when running manga-py; and wrapped it in \``` for better formatting.
- Make explicit all; writing what you know, create reproducible cases or simulations.
- Do not post screenshots; only plain text.
- Use the manga-py in latest version; see version running `$ manga-py -v`.
- If a old issue address your same question, continues writing on it:
    - write something like: `This affects me too, in the version 1.0. More information about this issue: ...`.
- Write One issue per (one) problem.
- Request features that many people wanna, not only you.

Requesting to add/support a *new* site
--------------------------------------

If you desire a new site to be supported by manga-py:

- Verify if your desired site is already supported:
    - https://manga-py.com/manga-py/
    - https://manga-py.github.io/manga-py/#resources-list
- Search through the `GitHub Issues`_ and `GitHub Pull Requests`_ if someone asked to add the same site.
- If nobody issued it, then submit your issue to add a new site.

Sponsoring
==========

To sponsor manga-py, please use the `GitHub Sponsor buttom`_.
It will list all modes to fund manga-py.

.. _`GitHub`: https://github.com/manga-py/manga-py/
.. _`GitHub Issues`: https://github.com/manga-py/manga-py/issues
.. _`GitHub Pull Requests`: https://github.com/manga-py/manga-py/pulls
.. _`GitHub repository`: https://github.com/manga-py/manga-py/blob/stable_1.x/CONTRIBUTING.rst
.. _`Code of Conduct`: https://github.com/manga-py/manga-py/blob/stable_1.x/docs/CODE_OF_CONDUCT.rst
.. _`GitHub Sponsor buttom`: https://github.com/manga-py/manga-py
.. _`PEP8`: https://www.python.org/dev/peps/pep-0008/
.. _`reStructuredText`: http://docutils.sourceforge.net/rst.html
.. _`GitHub Flavored Markdow`: https://help.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax
.. _`mentions`: https://help.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax#mentioning-people-and-teams
.. _`issue/pull-request references`: https://help.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax#referencing-issues-and-pull-requests
.. _`Python`: http://www.python.org/
.. _`install Python`: https://docs.python-guide.org/starting/installation/
.. _`install Git`: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
.. _`sign in GitHub`: https://help.github.com/en/github/getting-started-with-github/signing-up-for-a-new-github-account
.. _`add, commit and push`: https://help.github.com/en/github/managing-files-in-a-repository/adding-a-file-to-a-repository-using-the-command-line
.. _`pull request`: https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request
.. _`Docstrings`: https://www.python.org/dev/peps/pep-0257/
.. _`yapf`: https://github.com/google/yapf/#usage
.. _`pylint`: https://github.com/PyCQA/pylint
.. _`squash commits`: https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History
.. _`pull request template`: https://github.com/manga-py/manga-py/blob/templates/.github/PULL_REQUEST_TEMPLATE.md
