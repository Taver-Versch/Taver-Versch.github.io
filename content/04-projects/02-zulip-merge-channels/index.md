---
title: Zulip Merge Channels
meta: Spring 2026 | Course project | Team of 4
summary: Added a Merge Channels feature to Zulip, a large open-source team chat app, from GitHub issue #15634.
tags: Python, Django, TypeScript, Puppeteer, Agile Scrum
---
> **Note:** This was a project for a course, working on with a Team of 4 during my Spring 2026 Semester.

Zulip is an open-source, topic-based team chat app, kind of like Slack or Discord. Issue #15634 asked for a way to merge two channels, since similar channels were causing clutter and making messages harder to find. Here is a brief description of what we made, this was good experience working with a team to fix an issue.

## What we built
- A **Merge Channels** button with a dropdown to pick the destination channel.
- Every message, topic, reaction, star, and pinned message moves into the destination, so no history is lost.
- Users from the source channel get subscribed to the destination, and old links redirect.
- One message is posted in the destination's general topic, and only users who were in the source get a private notice.

## Permissions
We added a `can_merge_channels_group` field to the `UserGroup` model, so it works in the API like Zulip's other settings. Users need merge rights in both channels, and admins can hand out merge rights without making someone an admin.

## A decision we made
Zulip's old merge function archived the source channel. We chose to delete it instead, because merging is meant to be a one-way action. Undoing a merge would break the history once new messages are sent in the destination.

## Testing
Puppeteer tests cover the UI flow, and backend tests check source deletion, subscriptions carrying over, messages and topics moving, and the notification.
