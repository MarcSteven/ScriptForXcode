d "$(dirname "$0")/.."

if [[ -n "$CI" ]] || [[ $1 == "--fail-on-errors" ]] ; then
  FAIL_ON_ERRORS=true
  echo "Running in --fail-on-errors mode"
  ERROR_START=""
  COLOR_END=""
  INFO_START=""
else
  echo "Running in local mode"
  ERROR_START="\e[31m"
  COLOR_END="\e[0m"
  INFO_START="\e[34m"
fi

final_status=0
PODS_ROOT=${PODS_ROOT:-"Pods"}
PROJECT_DIR=${PROJECT_DIR:-$(pwd)}
# Needed for SwiftGen
export PRODUCT_MODULE_NAME=${PRODUCT_MODULE_NAME:-"YourProjectModuleName"}

if [[ `xcode-select -p` =~ CommandLineTools ]] ; then 
    echo "${ERROR_START}Your toolchain won't run Swiftlint or Sourcery. Use\n    sudo xcode-select -s /path/to/Xcode.app\nto fix this.${COLOR_END}"
fi

function process() {
  echo "\n${INFO_START}# Running $1 #${COLOR_END}"
  local initial_git_diff=`git diff --no-color`
  local start=`date +%s`
  
  eval "$2"

  if [ "$FAIL_ON_ERRORS" = "true" ] && [[ "$initial_git_diff" != `git diff --no-color` ]]
  then
    echo "${ERROR_START}$1 generates git changes, run './Scripts/workflow.sh' and review the changes${COLOR_END}"
    final_status=1
  fi

  local end=`date +%s`
  echo Execution time was `expr $end - $start` seconds.
}

function process_return_code() {
  echo "\n${INFO_START}# Running $1 #${COLOR_END}"
  eval "$2"
  local return_value=$?
  if [ "$FAIL_ON_ERRORS" = "true" ] && [ "$return_value" != "0"  ];
  then
    echo "${ERROR_START}$1 failed${COLOR_END}"
    final_status=1
  fi
}

function process_output() {
  echo "\n${INFO_START}# Running $1 #${COLOR_END}"
  local start=`date +%s`
  
  local output=$(eval "$2")

  if [[ ! -z "$output" ]]
  then
    echo "${ERROR_START}$1 reports issues:\n-----\n$output\n-----\nrun './Scripts/workflow.sh' and fix them${COLOR_END}"
    
    if [ "$FAIL_ON_ERRORS" = "true" ] 
    then
      final_status=1
    fi
  fi

  local end=`date +%s`
  echo Execution time was `expr $end - $start` seconds.
}


process "Sourcery" "${PODS_ROOT}/Sourcery/bin/sourcery --prune --quiet"
process "SwiftGen Storyboards" "${PODS_ROOT}/SwiftGen/bin/swiftgen storyboards -t scenes-swift4 ${PROJECT_DIR}/YourProject --output ${PROJECT_DIR}/YourProject/Resources/CodeGen/Generated.Storyboards.swift &> /dev/null"
process "SwiftGen Assets" "${PODS_ROOT}/SwiftGen/bin/swiftgen xcassets -t swift4 ${PROJECT_DIR}/YourProject/Resources/design-assets.xcassets --output ${PROJECT_DIR}/YourProject/Resources/CodeGen/Generated.Assets.swift &> /dev/null"
process "SwiftFormat" "${PODS_ROOT}/SwiftFormat/CommandLineTool/swiftformat . --quiet"
process_output "SwiftLint" "${PODS_ROOT}/SwiftLint/swiftlint lint --quiet"

if [[ $final_status -gt 0 ]]
then
  echo "\n${ERROR_START}Changes required. Run './Scripts/process.sh' and review the changes${COLOR_END}"
fi

exit $final_status
