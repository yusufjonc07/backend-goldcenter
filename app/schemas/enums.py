from enum import Enum

class EmployeeRoles(str, Enum):
  director = "director"
  accountant = "accountant"
  headConstructor = "headConstructor"
  constructor = "constructor"
  guard = "guard"
  headGuard = "headGuard"
  headCleaner = "headCleaner"
  cleaner = "cleaner"
  clerk = "clerk"

class FloorTypes(str, Enum):
  rent = "rent"
  personal = "personal"

class MessageTypes(str, Enum):
  text = "text"
  image = "image"
  video = "video"
  audio = "audio"

class ChatTypes(str, Enum):
  headConstructor = "headConstructor"
  headGuard = "headGuard"
  headCleaner = "headCleaner"

class ExpenceTypes(str, Enum):
  none = "none"
  forFloor = "forFloor"
  forBranch = "forBranch"

class UserRoles(str, Enum):
  director = "director"
  accountant = "accountant"
  headConstructor = "headConstructor"
  headGuard = "headGuard"
  headCleaner = "headCleaner"
  clerk = "clerk"