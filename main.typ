// Local entry point: compile this file from the repository root.
#import "lib.typ": fydp-report, guidance
#import "template/project.typ": project

#show: fydp-report.with(..project, logo: image("uiu.png", width: 28mm))

#include "template/content.typ"
