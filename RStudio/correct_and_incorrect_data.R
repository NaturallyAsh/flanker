raw_path <- 'raw_group_data.csv'
raw_data <- read_csv(raw_path)

raw_data <- raw_data %>% drop_na(Reaction_time)
raw_data <- raw_data %>% filter(Reaction_time > 0.250 & Reaction_time < 1.000)

raw_aov <- ANOVA(formula = Reaction_time ~ Group,
                 data = raw_data,
                 postHoc = ~ Group,
                 effectSize = "eta",
                 emMeans = ~ Group,
                 emmPlots = FALSE,
                 emmPlotError = 'none')

raw_descript <- descriptives(formula = Reaction_time ~ Group,
                             data = raw_data,
                             vars = c('Reaction_time', 'Accuracy'),
                             missing = FALSE,
                             median = FALSE,
                             sd = TRUE,
                             se = TRUE)
