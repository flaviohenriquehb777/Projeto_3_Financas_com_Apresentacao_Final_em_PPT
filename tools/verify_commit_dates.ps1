Param(
  [int]$Count = 5
)

git log -n $Count --pretty=format:"%h | %ad | %an | %s" --date=iso