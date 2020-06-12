exclude_path = '/Users/macuser/Documents/PYTHON:java/testing/sis/excluded_data.csv'
All_exclude_df = read_csv(exclude_path)

All_exclude_df <- All_exclude_df %>% rename("Reaction_time" = "Reaction time")
#filtered RT outliers
All_exclude_df <- All_exclude_df %>% filter(Reaction_time > 0.250 & Reaction_time < 1.000)
All_exclude_df$Group <- as_factor(All_exclude_df$Group)
All_exclude_df$Group <- fct_recode(All_exclude_df$Group, "NPF" = "A", "CPF" = "B", "NCPF" = "C")

# all_data_aov <- All_exclude_df %>% select(Group, "Reaction_time" = "Reaction time") 
  
#filtered RT outliers
# all_data_aov <- all_data_aov %>% filter(Reaction_time > 0.250 & Reaction_time < 1.000)

# all_data_aov$Group <- as_factor(all_data_aov$Group)

# all_data_aov$Group <- fct_recode(all_data_aov$Group, "NPF" = "A", "CPF" = "B", "NCPF" = "C")




#Jamovi ANOVA/Tukey 
data_aov <- ANOVA(formula = Reaction_time ~ Group,
                  data = All_exclude_df,
                  postHoc = ~ Group,
                  effectSize = "eta",
                  emMeans = ~ Group,
                  emmPlots = TRUE,
                  emmPlotError = 'ci')


data_aov



