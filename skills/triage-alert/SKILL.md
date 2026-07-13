---
name: triage-alert
description: Use when the user wants to triage an alert or decide how to respond to one.
---

# Triage an Alert

Decide fast, but show the reasoning. Every conclusion must name the signal it is based on.

## Step 1: Severity

Classify severity by user-facing impact, not by which metric fired.

A 2s p99 latency increase on checkout is more important than a crashed batch job with no customer impact.

State the trend:

- getting worse
- stable
- recovering

## Step 2: Blast radius

Identify which services and customer segments are affected.

Check dependencies in both directions:

- what this service calls
- what calls this service

## Step 3: Recent changes

Check deploys, config changes, and feature-flag flips in the last hour before considering exotic causes.

Most incidents follow a change.

## Step 4: Page or ticket

Page if user-facing impact is active or the trend is worsening.

Create a ticket if the impact is past, contained, or the alert is a known false positive.

Never page on a metric alone.

## Output

Return:

- **Severity**: level, with the one signal that decided it
- **Blast radius**: services and customer segments affected
- **Suspected cause**: the most recent correlated change, if any
- **Decision**: page or ticket, and the first status update to send