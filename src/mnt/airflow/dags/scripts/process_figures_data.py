
#import findspark
#findspark.init()
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
#Initialize Spark Session
def main():
    spark = SparkSession \
        .builder \
        .appName("Figures processing") \
        .config("spark.jars", "/opt/spark/jars/postgresql-42.2.5.jar") \
        .getOrCreate()

    sdf = spark.read.option("multiline","true").json(r'/opt/airflow/dags/files/fgb_figures_prices.json')

    sdf = sdf.withColumn("Availability_str", F.split(F.col("Status"), ":").getItem(1))
    sdf = sdf.withColumn("Availability", F.when(F.col("Availability_str")
                                                .cast("int").isNotNull(), F.col("Availability_str"))
                                            .otherwise(0))
    sdf = sdf.withColumn("Comments", F.when(F.col("Availability_str")
                                              .cast("int").isNotNull(), "Dostępny")
                                         .otherwise(F.col("Availability_str")))
    sdf = sdf.withColumn("Availability",F.col("Availability").cast("int"))
    sdf = sdf.withColumn("Price",F.col("Price").cast("double"))
    sdf = sdf.withColumn("Download",F.to_date(F.col("Download"), "yyyy-MM-dd"))
    sdf = sdf.drop("Availability_str", "Status")


    sdf1 = spark.read.option("multiline","true").json(r'/opt/airflow/dags/files/mtg_figures_prices.json')
    sdf1 = sdf1.withColumn("Availability", F.when(F.col("Status")
                                                .cast("int").isNotNull(), F.col("Status"))
                                            .otherwise(0))
    sdf1 = sdf1.withColumn("Comments", F.when(F.col("Status")
                                              .cast("int").isNotNull(), "Dostępny")
                                         .otherwise(F.col("Status")))
    sdf1 = sdf1.withColumn("Price",F.col("Price").cast("double"))
    sdf1 = sdf1.withColumn("Availability",F.col("Availability").cast("int"))
    sdf1 = sdf1.withColumn("Download",F.to_date(F.col("Download"), "yyyy-MM-dd"))
    sdf1 = sdf1.drop("Status")

    sdf_final = sdf.unionByName(sdf1)


    sdf_final.coalesce(1) \
      .write \
      .option("header","true") \
      .option("sep",",") \
      .mode("overwrite") \
      .csv(r'/opt/airflow/dags/files/figures_prices.csv')

    # Write to MySQL Table
    # if data should be overwritten
    #  .option("truncate", "true") \
    #  .mode("overwrite") \
    sdf_final.write \
      .mode("append") \
      .format("jdbc") \
      .option("driver","org.postgresql.Driver") \
      .option("url", "jdbc:postgresql://postgres:5432/airflow_db") \
      .option("dbtable", "figures_details") \
      .option("user", "airflow") \
      .option("password", "airflow") \
      .option("encoding", "UTF-8") \
      .save()

if __name__ == "__main__":
    main()