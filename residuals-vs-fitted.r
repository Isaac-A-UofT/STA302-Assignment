#load the dataset
library(readxl)
school_data <- read_excel("302Assignment/school_data.xlsx")

school_data <- na.omit(school_data)

#Also have: Carnegie Classification (Undergraduate), Carnegie Size Setting, School Locale

# Fit a regression model
model <- lm(`Median Salary (1 Year After Graduation)` ~ 
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

fitted_values = fitted(model)
residual_values = resid(model)
price_values = school_data$`Median Salary (1 Year After Graduation)`

# Create a new dataset excluding the 25 largest fitted values
sorted_indices <- order(fitted_values, decreasing = TRUE)
indices_to_remove <- sorted_indices[1:25]

# Filter out the 50 largest fitted values from the data for plotting
fitted_values_filtered <- fitted_values[-indices_to_remove]
price_values_filtered <- price_values[-indices_to_remove]
residual_values_filtered <- residual_values[-indices_to_remove]



# Create the price vs regression plot
plot(fitted_values, price_values,
     main = "Price versus regression fit",
     xlab = "Fitted values", ylab = "Median Salary (1 Year After Graduation)")
abline(0, 1,
       col="blue", lty=1)
legend("bottomright", legend=c("y = x line"),
       col="blue", lty=1)



# Create the price vs regression plot excluding the 25 largest fitted values
plot(fitted_values_filtered, price_values_filtered,
     main = "Price versus regression fit (Excluding 25 Largest Fitted Values)",
     xlab = "Fitted values", ylab = "Median Salary (1 Year After Graduation)")
abline(0, 1,
       col="blue", lty=1)
legend("bottomright", legend=c("y = x line"),
       col="blue", lty=1)


#Fitted vs residual
plot(fitted_values, residual_values, 
     main = "Salary after graduation: fitted versus residual values", 
     xlab = "Fitted", 
     ylab = "Residuals")



#Fitted vs residual excluding the 25 largest fitted values
plot(fitted_values_filtered, residual_values_filtered, 
     main = "Salary after graduation: fitted versus residual values excluding the 25 largest fitted values", 
     xlab = "Fitted", 
     ylab = "Residuals")

plot(model, which=1)



#Fitted vs sresidual
sresidual_values = rstandard(model)

plot(fitted_values, sresidual_values, 
     main = "Salary after graduation: fitted versus residual values", 
     xlab = "Fitted", 
     ylab = "Residuals")



#Fitted vs sresidual excluding the 25 largest fitted values
sresidual_values = rstandard(model)
sresidual_values_filtered <- sresidual_values[-indices_to_remove]

plot(fitted_values_filtered, sresidual_values_filtered, 
     main = "Salary after graduation: fitted versus residual values excluding the 25 largest fitted values", 
     xlab = "Fitted", 
     ylab = "Residuals")

plot(model, which=3)

