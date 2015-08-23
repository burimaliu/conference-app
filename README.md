# Conference App (API project)

### About

This project is a cloud-based API server to support a web-based and native mobile applications for conference organization.

This is a cloud-based server side API to fullfil a web-based and native mobile applications conference needs. The API's supports the following:

- Authentication (Google accounts)
- Session
- Profiles
- User wishlist's
- Conference's

Project is hosted on Google App Engine as application ID [conference-app-1040](https://conference-app-1040.appspot.com), and can be accessed via the [API explorer](https://apis-explorer.appspot.com/apis-explorer/?base=https://conference-app-1040.appspot.com/_ah/api#p/).

### Improvements

####  1: Add Sessions to a Conference

The following methods were added:

- `createSession`: for a given conference, creates a session.
- `getConferenceSessions`: for a given conference, returns all sessions.
- `getConferenceSessionsByType`: for a given conference with session type, returns all applicable sessions.
- `getSessionsBySpeaker`: for a given speaker, returns all sessions across all conferences.

For the `Session` model, The following datastore properties were implemented:


| Property        | Type                     | Explanation                                                                    |
|-----------------|:-------------------------|:-------------------------------------------------------------------------------|
| name            | StringProperty(required)  | Name is a short text that stores user's name and it should be a string         |
| highlights      | StringProperty           | Highlights have a mixed values, to avoid errors decited to set it as string    |
| speaker         | StringProperty(required)  | Represents Speaker's name and since it does only that it should be a string    |
| duration        | IntegerProperty          | Duration contains number thus it should be an Integer eg: "15" minutes |
| typeOfSession   | StringProperty(repeated)  | Session type usually has multiple choices, however in this case we are storing only one type and string is fine |
| date            | DateProperty             | Date stores conference date, DateType because its only "Date" value and can be used to filter data based on its value |
| startTime       | TimeProperty             | Start time would show only time of a conference session, set to TimeProperty since it stores only Time values |
| organizerUserId | StringProperty           | String was chosen to store ID of conference organizatior, Integer could also be possible |

To represent the one `conference` to many `sessions` relationship, A parent-child was implemented which allows for more consistent querying as sessions can be queried by their conference ancestor. Sessions were `Memcached` also.

To represent speakers it was possible to link `speaker` field with user profile, however that would require a speaker to have an account, having just its name was more reasonable even it could produce undesirable results.

Session types (e.g. speech, lecture) were implemented more as "tags" representation, so sessions will be able to receive multiple types.

#### 2: Add Sessions to User Wishlist

The `Profile` model was modified to accommodate 'wishlist' stored as a repeated key property field, named `sessionsToAttend`.  The following endpoint methods were added to API:

- `addSessionToWishlist`: given a session websafe key, saves a session to a user's wishlist.
- `getSessionsInWishlist`: return a user's wishlist.

#### 3: Indexes and Queries

The follwing endpoint methods that would be useful to this application:

-`getConferenceSessionFeed`: returns a conference's sorted feed sessions occurring same day or later.

-`getTBDSessions`: returns sessions with missing time/date. Useful to let conference creators know that certain sessions have lack of information.

To filter non-workshop before 7pm sessions using Datastore queries ran on its limitations since it allows only one inequality filter, as a result an alternative was to first filter all sessions before 7pm using `ndb` of datastore and then iterating through the list and picking up those with `workshop`.

#### 4: Add Featured Speaker

It was necessary to modify the `createSession` endpoint to cross-check if the speaker was in any other of the conference's sessions. If true, the speaker name and relevant session names were added to the memcache under the `featured_speaker` key.

<<<<<<< HEAD
The following endpoint method `getFeaturedSpeaker` was added which would check the memcache for the featured speaker.
=======
The following endpoint method: `getFeaturedSpeaker` was added which would check the memcache for the featured speaker.
>>>>>>> origin/master

### Setup Instructions

To deploy this API server locally, ensure that you have downloaded and installed the [Google App Engine SDK for Python](https://cloud.google.com/appengine/downloads). Once installed, conduct the following steps:

1. Clone `conference-app` repository.
2. (Optional) Update the value of `application` in `app.yaml` to the app ID you have registered in the App Engine admin console and would like to use to host your instance of this sample.
3. (Optional) Update the values at the top of `settings.py` to reflect the respective client IDs you have registered in the [Developer Console][4].
4. (Optional) Update the value of CLIENT_ID in `static/js/app.js` to the Web client ID
5. (Optional) Mark the configuration files as unchanged as follows: `$ git update-index --assume-unchanged app.yaml settings.py static/js/app.js`
6. Run the app with the devserver using `dev_appserver.py DIR`, and ensure it's running by visiting your local server's address (by default [localhost:8080][5].)
7. (Optional) Generate your client library(ies) with [the endpoints tool][6].
8. (Optional) Deploy the application via `appcfg.py update`.

### Resources

- [Google App Engine Python Docs](https://cloud.google.com/appengine/docs/python/)
- [Data Modeling for Google App Engine Using Python and ndb (Screencast)](https://www.youtube.com/watch?v=xZsxWn58pS0)
