// Local entry point: compile this file from the repository root.
#import "lib.typ": fydp-report, guidance
#import "template/project.typ": project

// Optional local logo: typst compile --input logo=local-assets/uiu.png main.typ
#let logo-path = sys.inputs.at("logo", default: none)
#show: fydp-report.with(..project, logo: if logo-path == none { none } else { image(logo-path, width: 28mm) })

#include "template/content.typ"
