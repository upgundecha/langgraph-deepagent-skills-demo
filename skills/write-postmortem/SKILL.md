---
name: write-postmortem
description: Use when the user wants to write a postmortem for a resolved incident.
---

# Write a Postmortem

Write in a blameless style. Name systems and gaps, never people.

If a draft sentence contains a person's name next to a mistake, rewrite it.

## Step 1: Timeline from records

Build the timeline from logs, deploy history, and alert timestamps, not from memory.

Mark every entry that could not be confirmed from a record.

## Step 2: Contributing factors

List at least two contributing factors.

Single root causes are usually the last factor noticed, not the only factor involved.

For each factor, state which safeguard was missing or failed.

## Step 3: What limited the damage

Record what went well and what was luck.

Luck is a gap wearing a disguise.

## Step 4: Action items

Each action item needs an owner and a test.

For each item, state whether it would have:

- prevented the incident
- shortened the incident
- improved detection

Drop items that do none of these.

## Output

Return:

- **Summary**: impact, duration, detection method, one paragraph
- **Timeline**: timestamped entries, with unconfirmed entries marked
- **Contributing factors**: each with the missing safeguard
- **Action items**: owner, prevent-or-shorten label, due date