library(readxl)
school_data <- read_excel("302Assignment/school_data.xlsx")

# Fit a regression model
model <- lm(`Median Salary (2 Years After Graduation)` ~ 
              `Student Size` + 
              `In-State Tuition` + 
              `Completion Rate` + 
              `Overall Admission Rate` + 
              `Average SAT Score` + 
              `Student-Faculty Ratio` + 
              `Gender Shannon Index` +
              `Diversity Index` +
              `Endowment`,
            data = school_data)

hist(rstandard(model),
     main = "Standardized residuals histogram",
     xlab = "Standardized residuals")
abline(0, 1)

plot(model, which=2)