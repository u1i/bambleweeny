# User Stories & Notes

| Story | Description |
| :---: | :--- | 
| 1 | As a platform user, I need to authenticate with an email address and password |
| 2 | As a platform user, I need be able to create, list and delete resources |
| 3 | As a platform user, I should not be able to access resources owned by other users |
| 4 | As a platform user, I should not be able to create a new resource if the quota is exceeded |
| 5 | As a platform administrator, I should be able to create, list and delete users and their resources |
| 6 | As a platform administrator, I should be able to set the quota for any user |

## Notes

* A resource is represented by a string with a unique identifier
* Platform administrator is a platform user as well
* By default, the quota is not set, which means a user can create as many resources as he wants
* The system should provide responses for any errors that might occur
