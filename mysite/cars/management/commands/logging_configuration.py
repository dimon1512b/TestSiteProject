LOGGING = {
	"version": 1,
	"handlers": {
		"fileHandler_1": {
			"class": "logging.FileHandler",
			"formatter": "myFormatter_1",
			"filename": "log_parse_auto.log",
			"level": "INFO",
			"encoding": "UTF-8"
		}
	},
	"loggers": {
		"parse": {
			"handlers": ["fileHandler_1"],
			"level": "INFO"
		}
	},
	"formatters": {
		"myFormatter_1": {
			"format": "%(asctime)s - %(levelname)s - %(message)s"
		},
		"myFormatter_2": {
			"format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s"
		},
		"myFormatter_3": {
			"format": "%(name)s - %(filename)s - %(levelname)s - %(funcName)s - %(message)s"
		}
	}
}
