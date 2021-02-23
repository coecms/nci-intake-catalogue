GEN := $(wildcard */generate.sh)
CATS := $(addsuffix /catalogue.csv,$(dir ${GEN}))

all: ${CATS}

%/catalogue.csv: %/generate.sh %/catalogue.json 
	pushd $*; ./generate.sh
