#! usr/bin/env python3
import logging

logging.getLogger('spine').addHandler(logging.NullHandler())

import AttachmentLoader
import Enum
from Attachment import Attachment
from Atlas import *
from RegionAttachment import *
from Skeleton import *


