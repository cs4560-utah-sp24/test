Your CS 4560 Final Project
==========================

CS 4560 requires a final project worth 30% of your overall course
grade. You will work on the final project in groups of 4. Some class
time will be provided for coordination between group members, but you
and your group are also encouraged to find time outside class hours to
work together.

Timeline and Grading
--------------------

The class project will proceed on this timeline:

Project groups will be announced on **March 18**. Groups will be
formed by the professor: you typically do not get the choice to work
with only your pre-existing friends out in the professional world.
However, if for personal reasons you wouldn't be able to work with
another class member, you can express that on a quiz and the professor
will take that into account.

On **April 11**, you must have a group member in class to report to
the professor what type of project your group is planning to do. If
you're planning to do a custom proposal you should be ready to share
your detailed project proposal. These are graded on timeliness and
worth one sixth of the project grade (so 5% of your final grade),
except for the custom proposal (see below).

On **April 16**, you must have a group member in class to report to
the professor on initial progress. This is typically going to be
initial explorations of the bugs tracker and draft tests or perhaps
progress getting a web browser engine compiled. You are graded on
having made *some* progress, worth one sixth of the project grade (so
5% of your final grade).

On **April 23**, project submissions are due. What you submit depends
on the project type. If you are working on a Ladybird, browser engine,
or web infrastructure project, your submission is little more than
links to any submitted bugs or pull requests. If you are working on a
custom proposal, the submission is expected to be more substantial;
see below. The project submission is graded on results and is worth
two thirds of the project grade (so 20% of your final grade).

Collaboration
-------------

All group members are expected to contribute to the group project. We
**strongly recommend working synchronously on the project**, much like
you worked together in class. Real-world web browsers are challenging,
and four people working together are more likely to make progress than
four people working separately.

It is thus imperative that you **schedule a fixed time to work on the
project**. Time in class will not be sufficient (though we encourage
you to use that time, too). Schedule a regular weekly session of at
least four hours that all group members can attend.

In rare cases, a group member will not contribute equally to their
group's project. If this happens, group members will be able to note
this during project submission and the professor may adjust grades in
response.

Project Types
-------------

Four types of projects are envisioned, described below. Groups are
encouraged to read all four and pick the project that appeals to them
most. Groups that can't decide or have no strong preference should
choose the first type, a Ladybird project.

## Project Type: Ladybird

This project type, in honor of this year's guest speaker, involves
contributions to the [Ladybird browser engine](https://ladybird.dev/)
or [SerenityOS libraries](https://serenityos.org/) that it depends on.
The Ladybird browser is a new browser engine in active development.

Because it is still a young browser project, it has many obvious bugs
and avenues for improvement. The Ladybird project posts monthly
updates on Youtube (found on the website); project members are
encouraged to watch a recent one to see what areas are under active
development. Project groups are also encouraged to join the
[SerenityOS Discord](https://discord.gg/serenityos) to introduce
themselves and get help if necessary.

In this project type, project members download and build the [Ladybird
browser engine](https://ladybird.dev/). They then find, minimize, and
report bugs in the Ladybird browser engine to the [Ladybird bug
tracker](https://github.com/SerenityOS/serenity/issues). The project
group would then fix the bugs. Project members might want to read a
[blog
post](https://t-shaped.nl/posts/understanding-complexity-like-an-engineer-the-case-of-the-ladybird-browser)
about the process of filing and fixing such bugs.

A successful project will find, minimize, report, and fix at least one
bug. Project members are encouraged to discuss with the professor
after minimizing and reporting but before trying to fix a bug, to help
determine if the bug is reasonably fixable or is perhaps too hard.

It's possible, though unlikely, that project members will find,
minimize, and report a number of bugs but not find any that seem
reasonably fixable; in this situation the professor may still award
full marks.

For this type of project, the project submission should link to all
submitted bugs and pull requests, unless instructed otherwise by the
professor.

## Project Type: Browser Engine

This project type envisions group members contributing code to one of
the three major browser engines: Blink (used in Chrome and Edge),
Gecko (used in Firefox), or Webkit (used in Safari). You can find
project ideas by browsing the browser engine bug trackers:

- [Monorail](https://issues.chromium.org/issues?q=status:open), the
  Blink/Chrome bug tracker, has a a "Hotlist" called `GoodFirstBug`;
  that means that if you type `Hotlist-GoodFirstBug status:new blink`
  into the search bar, you'll see bugs that the Chrome developers have
  checked and decided would be good first bugs.

- [Bugzilla](https://bugzilla.mozilla.org/describecomponents.cgi?product=Core),
  the Gecko/Firefox bug tracker, is broken down by component. Recent
  open bugs, especially those marked `UNCO` (meaning unconfirmed) or
  `NEW` (meaning not yet assigned to anyone) are good choices.

- [Webkit](https://bugs.webkit.org/describecomponents.cgi?product=WebKit)
  also uses Bugzilla so it too has a page listing components and can
  be browsed similarly to the Gecko/Firefox Bugzilla.

Some bugs are easy to fix and others are hard to fix. Pick the easy
ones! In each case, look for bugs that are sort-of recent (not over a
year old) with a clear bug report. Read the bug discussion---if
someone is already working on it, or worse has worked on it for a
while and found it to be very difficult, it's better to pick a
different bug.

Any code contribution more significant than, say, fixing typos in
comments is sufficient to get full credit for the project. Your code
does not necessarily have to be accepted and merged into the browser
you're contributing to to get full marks, though you do have to post a
high-quality patch. When you post a patch, it's a good idea to
indicate that you're a student; write something like:

> I'm a University of Utah student working on [engine] as part of my
> final project for CS 4560 Web Browser Internals.

That'll get you some nicer / more useful reviews.

Most code contributions won't be accepted without accompanying tests,
usually in WPT. Project groups are thus encouraged to first develop
and contribute WPT tests; see the next project type.

For this type of project, the project submission should link to all
submitted bugs and pull requests, unless instructed otherwise by the
professor.

## Project Type: Web Platform Tests

This project type envisions group members contributing to [Web
Platform Tests](https://web-platform-tests.org/). WPT is a
cross-browser test suite for the whole web platform. It is developed
[on Github](https://github.com/web-platform-tests/wpt). WPT includes
tests for all major components of a rendering engine; as of this
writing, it tests roughly 250 web features using a total of roughly
55,000 tests. It is the primary test suite for all three major browser
rendering engines (and Ladybird is also working on using it).

Despite the immense size of the test suite, there are many features
not well covered by it---that's why browsers still have bugs! In this
project type, group members would contribute new tests to WPT. Good
tests can be found by perusing the browser bug trackers linked to in
the previous project type. [PR
#44995](https://github.com/web-platform-tests/wpt/pull/44995) is an
example of one kind of possible contribution: a new test derived from
a reported browser bug.

Any high-quality test contribution is sufficient to get full credit
for the project. Your test does not necessarily have to be accepted to
get full marks, though you do have to post a high-quality patch.

For this type of project, the project submission should link to all
submitted bugs and pull requests, unless instructed otherwise by the
professor.

## Project Type: Custom

The last project type is a catch-all where the project group proposes
and then completes a significant browser development project of their
choice. Some possibilities include:

- Implementing a significant new browser feature in the textbook
  browser.
- Replacing some component of the textbook browser with a production
  implementation.
- Developing a static analysis tool for JavaScript or CSS.
- Developing a substantial change to existing browser developer tools,
  UIs, webdriver implementations, or other components outside the
  rendering engine itself.
- Contributing to other web infrastructure, including the WPT runner,
  the MDN documentation, or the standards process.

Since this project type is fully flexible, more and earlier
communication with the professor is a must. After discussing a project
idea informally, project groups doing a custom proposal must submit a
one-page project proposal describing the proposed development in some
detail, including the proposed code architecture (which classes /
methods will be modified or created), mockups of any new UI, and
identifying milestones that can used to check progress midway.
Milestones should be chosen so they can be achieved by the April 16
report date.

The project submission for this project type is a three-page writeup
of what was achieved. It should include a short motivation section, an
overview of the final code architecture, and screenshots of any new UI
or descriptions of tests run and their results. It should also include
a discussion of any challenges faced. The submission must link to the
completed code, posted somewhere the professor can access it.
