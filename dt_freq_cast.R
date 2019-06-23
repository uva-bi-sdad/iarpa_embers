library(data.table)
library(stringr)

fs <- list.files("data/embers/gizem_twitter/output files/brazil-hashtags/", pattern = "twit*", full.names = T)

if (exists("dtf") == TRUE) rm(dtf)
for (f in fs) {
  dt <- fread(f)
  dt <- dt[Freq > 10]
  dt$day <- str_match(f, "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]")[,1]
  if (exists("dtf") == FALSE) {
      dtf <- dt
    } else {
      dtf <- rbindlist(list(dtf, dt))
    }
}

dc <- dcast(dtf, yyy ~ day, value.var = "Freq")

dc[, Sum := rowSums(.SD, na.rm = TRUE), .SDcols = grep("[0-9][0-9][0-9][0-9]", names(dc))]
