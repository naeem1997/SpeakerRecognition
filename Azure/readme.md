Strengths:

support for custom speech and acoustic models
Developers can also code applications to deliver recognition results in real time; this could enable an application to give users feedback to speak more clearly or to pause when their words are not being properly recognized.

[Docs](https://azure.microsoft.com/en-us/services/cognitive-services/speaker-recognition/)

-API documentation and explains enrollment, verification, and recognition parts of ASR
  -Speaker Verification
-Speaker Verification APIs can automatically verify and authenticate users using their voice or speech.

  -Enrollment
  
-speaker's voice is recorded saying a specific phrase, then a number of features are extracted and the chosen phrase is recognized

Forms unique voice signature
Verification
an input voice and phrase are compared against the enrollment's voice signature and phrase
Speaker Identification
Speaker Identification APIs can automatically identify the person speaking in an audio file, given a group of prospective speakers (first you need to have speakers enrolled)
Enrollment
Recognition
The input voice is compared against all speakers in order to determine whose voice it is, and if there is a match found, the identity of the speaker is returned
REST API Calls List 

Speaker identification and verification- Strong

Cons:

Documentation can get quite disorganized but good doc nonetheless

Last commit was on March 2018, so perhaps not disorganized?

Actually tried it from the demo and there can be instances where it overfit enrollment data

[Rest API Calls List](https://westus.dev.cognitive.microsoft.com/docs/services/563309b6778daf02acc0a508/operations/563309b7778daf06340c9652)
