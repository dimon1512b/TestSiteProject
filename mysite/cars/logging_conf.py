LOGGING = {
	"version": 1,
	"handlers": {
		"fileHandler_1": {
			"class": "logging.FileHandler",
			"formatter": "myFormatter_1",
			"filename": "log_parse_auto.log",
			"level": "INFO",
			"encoding": "UTF-8"
		},
		"fileHandler_2": {
			"class": "logging.FileHandler",
			"formatter": "myFormatter_1",
			"filename": "log_view.log",
			"level": "INFO",
			"encoding": "UTF-8"
		}
	},
	"loggers": {
		"parse": {
			"handlers": ["fileHandler_1"],
			"level": "INFO"
		},
		"views": {
			"handlers": ["fileHandler_2"],
			"level": "DEBUG"
		}
	},
	"formatters": {
		"myFormatter_1": {
			"format": "%(asctime)s - %(funcName)s - %(message)s"
		},
		"myFormatter_2": {
			"format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s"
		},
		"myFormatter_3": {
			"format": "%(name)s - %(filename)s - %(levelname)s - %(funcName)s - %(message)s"
		}
	}
}
