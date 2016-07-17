managers_schema = {
    'name': {
        'type': 'string',
        'required': True,
    },
    'description': {
        'type': 'string',
    },
    'picture': {
        'type': 'string',
    },
    'host': {
        'type': 'string',
        'required': True
    }
}

jobs_schema = {
    'name': {
        'type': 'string',
        'required': True,
    },
    # Defines how we are going to parse the settings field, in order to generate
    # the tasks list.
    'job_type': {
        'type': 'string',
        'required': True,
    },
    # Remarks about the settings, the author or the system
    'notes': {
        'type': 'string',
    },
    'project': {
         'type': 'objectid',
         'data_relation': {
            'resource': 'projects',
            'field': '_id',
            'embeddable': True
         },
    },
    'user': {
        'type': 'objectid',
        'required': True,
        'data_relation': {
            'resource': 'users',
            'field': '_id',
            'embeddable': True
        },
    },
    # We currently say that a job, and all its tasks, will be assigned to one
    # manager only. If one day we want to allow multiple managers to handle a
    # job we can convert this to a list.
    'manager': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'managers',
            'field': '_id',
            'embeddable': True
        },
    },
    'status': {
        'type': 'string',
        'allowed': [
            'completed',
            'active',
            'canceled',
            'queued',
            'failed'],
        'default': 'queued'
    },
    # This number could be also be a float between 0 and 1.
    'priority': {
        'type': 'integer',
        'min': 1,
        'max': 100,
        'default': 50
    },
    # Embedded summary of the status of all tasks of a job. Used when listing
    # all jobs via a graphical interface.
    'tasks_status': {
        'type': 'dict',
        'schema': {
            'count': {'type': 'integer'},
            'completed': {'type': 'integer'},
            'failed': {'type': 'integer'},
            'canceled': {'type': 'integer'}
        }
    },
    # The most important part of a job. These custom values are parsed by the
    # job compiler in order to generate the tasks.
    'settings': {
        'type': 'dict',
        # TODO: introduce dynamic validator, based on job_type/task_type
        'allow_unknown': True,
    }
}

tasks_schema = {
    'job': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'jobs',
            'field': '_id',
            'embeddable': True
        },
    },
    'manager': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'managers',
            'field': '_id',
            'embeddable': True
        },
    },
    'name': {
        'type': 'string',
        'required': True,
    },
    'status': {
        'type': 'string',
        'allowed': [
            'completed',
            'active',
            'canceled',
            'queued',
            'processing',
            'failed'],
        'default': 'queued'
    },
    'priority': {
        'type': 'integer',
        'min': 1,
        'max': 100,
        'default': 50
    },
    'job_type': {
        'type': 'string',
        'required': True,
    },
    'parser': {
        'type': 'string',
        'required': True,
    },
    'settings': {
        'type': 'dict',
        # TODO: introduce dynamic validator, based on job_type/task_type
        'allow_unknown': True,
    },
    'log': {
        'type': 'string',
    },
    'activity': {
        'type': 'string',
        'maxlength': 128
    },
    'parents': {
        'type': 'list',
        'schema': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'tasks',
                'field': '_id',
                'embeddable': True
            }
        },
    },
    'worker': {
        'type': 'string',
    },
}

managers = {
    'schema': managers_schema,
}

jobs = {
    'schema': jobs_schema,
}

tasks = {
    'schema': tasks_schema,
}