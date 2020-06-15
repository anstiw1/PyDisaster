# PyDisaster

## Problem 8: Crowdsourcing Damage Photos

### Problem Statement: 
 Imagery is scarce at the start of a disaster. FEMA and partners rely on photos and other imagery to understand the disaster impacts and validate reports of damage. However, it is almost impossible to systematically acquire imagery the first day. Within the first few days, FEMA typically receives several types of satellite data. Within a week, other aerial imagery becomes available. Photos posted to social media can help fill in gaps in the interim, but these images are not captured systematically. The entire emergency management community would benefit from an app or service that anyone in an impacted area could use to take and submit photos. Ideally, these photos could be attained with cameras people may have on them (e.g. iPhones) or low-cost cameras. We need a systematic image capture workflow in order to conduct AI/ML/edge computing to conduct damage assessments. (Doing this from the ground would probably be quicker/easier than waiting on the winds to dissipate so you can fly planes.)

### Proposed Deliverables:
During disasters, FEMA needs to know the exact location of the damaged places. It is crucial to pinpoint a place and evaluate the damage when dispatching the resources. Our PyDisaster project can help to extract GPS location from photos submitted to our___ (...website/app?) using AI/ML/edge computing technology. This will allow FEMA to conduct damage assessments in those effected areas.

### Required Installations:
Imports: pandas, requests, os, io, json

from bs4 import BeautifulSoup

from google.cloud import vision

from google.cloud.vision import types

from google.oauth2 import service_account

from flask import Flask, render_template, request

from werkzeug.utils import secure_filename

from PIL import Image

from PIL.ExifTags import TAGS, GPSTAGS

### Workflow:


### Executive Summary:
