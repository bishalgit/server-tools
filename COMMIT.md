# How to Write a Git Commit Message

> This article gives guidelines to a developer for writing a good and efficient commit message in git so that other developers who will maintain the code or join the team later get the detail understanding about the project.

## Introduction: Why good commit messages matter

If you want to get the full understanding of why good commit is required read this [section of Article](https://chris.beams.io/posts/git-commit/#intro). Skip this if you already know why good commit messages matter.

## The seven rules of a great Git commit message

1. Separate subject from body with a blank line
2. Limit the subject line to 50 characters
3. Capitalize the subject line
4. Do not end the subject line with a period
5. Use the imperative mood in the subject line
6. Wrap the body at 72 characters
7. Use the body to explain what and why vs. how

For example:

```
Summarize changes in around 50 characters or less

More detailed explanatory text, if necessary. Wrap it to about 72
characters or so. In some contexts, the first line is treated as the
subject of the commit and the rest of the text as the body. The
blank line separating the summary from the body is critical (unless
you omit the body entirely); various tools like `log`, `shortlog`
and `rebase` can get confused if you run the two together.

Explain the problem that this commit is solving. Focus on why you
are making this change as opposed to how (the code explains that).
Are there side effects or other unintuitive consequences of this
change? Here's the place to explain them.

Further paragraphs come after blank lines.

 - Bullet points are okay, too

 - Typically a hyphen or asterisk is used for the bullet, preceded
   by a single space, with blank lines in between, but conventions
   vary here

If you use an issue tracker, put references to them at the bottom,
like this:

Resolves: #123
See also: #456, #789
```

> This commit from Bitcoin Core is a great example of explaining what changed and why:

```
commit eb0b56b19017ab5c16c745e6da39c53126924ed6
Author: Pieter Wuille <pieter.wuille@gmail.com>
Date:   Fri Aug 1 22:57:55 2014 +0200

   Simplify serialize.h's exception handling

   Remove the 'state' and 'exceptmask' from serialize.h's stream
   implementations, as well as related methods.

   As exceptmask always included 'failbit', and setstate was always
   called with bits = failbit, all it did was immediately raise an
   exception. Get rid of those variables, and replace the setstate
   with direct exception throwing (which also removes some dead
   code).

   As a result, good() is never reached after a failure (there are
   only 2 calls, one of which is in tests), and can just be replaced
   by !eof().

   fail(), clear(n) and exceptions() are just never called. Delete
   them.
```

## Tips

### Learn to love the command line. Leave the IDE behind.

> For as many reasons as there are Git subcommands, it’s wise to embrace the command line. Git is insanely powerful; IDEs are too, but each in different ways. I use an IDE every day (IntelliJ IDEA) and have used others extensively (Eclipse), but I have never seen IDE integration for Git that could begin to match the ease and power of the command line (once you know it).

> Certain Git-related IDE functions are invaluable, like calling git rm when you delete a file, and doing the right stuff with git when you rename one. Where everything falls apart is when you start trying to commit, merge, rebase, or do sophisticated history analysis through the IDE.

> When it comes to wielding the full power of Git, it’s command-line all the way.

> Remember that whether you use Bash or Zsh or Powershell, there are tab completion scripts that take much of the pain out of remembering the subcommands and switches.

## Read Pro Git

The [Pro Git](https://git-scm.com/book/en/v2) book is available online for free, and it’s fantastic. Take advantage!


## Acknowledgements
* **[Chris Beams](https://disqus.com/home/forums/cbeams/)** - For full detailed article visit [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/#intro) 