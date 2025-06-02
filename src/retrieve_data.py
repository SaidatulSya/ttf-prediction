from cognite.client import CogniteClient
from datetime import datetime
import pandas as pd
 
 
class RetrieveData:
    """Retrieve data of one pi tag with any desidered aggregation method within a time frame. Has method to convert results into pandas dataframe
    """
    def __init__(self, client: CogniteClient):
        self.client = client
        self.pitag = None
        self.ext_id = None
        self.agg = None
 

    def retrieve_agg(self, ex_id, start_time_str, end_time_str, agg, interval):

        #store external_id and aggregation method into attribute as reference
        self.ext_id = ex_id
        self.agg = agg
        
        # Extract tag name for file saving
        raw_tag = ex_id.split(".")[-1]
        self.pitag = raw_tag.replace(".", "_")
    
        # # Convert to datetime
        # now = datetime.utcnow()
        # start_dt = pd.to_datetime(start_time_str)
        # end_dt = pd.to_datetime(end_time_str)
    
        # # Calculate timedelta differences
        # delta_start = now - start_dt
        # delta_end = now - end_dt
    
        # # Convert timedelta to number of days/hours ago
        # start_shift = f"{int(delta_start.total_seconds() // 86400)}d-ago"
        # end_shift = f"{int(delta_end.total_seconds() // 86400)}d-ago"
    
        # Retrieve datapoints
        datapoints = self.client.time_series.data.retrieve(
            external_id=ex_id,
            start=start_time_str,
            end=end_time_str,
            aggregates=agg,
            granularity=interval
        )
    
        df = datapoints.to_pandas()

        #rename columns
        df = df.rename(columns={df.columns[0]:"value"})
        df = df.reset_index()
        df.columns = ["Timestamp", "value"]
        return df

    def retrieve_raw(self, ex_id, start_time, end_time):
        raw_data = self.client.time_series.data.retrieve(
            external_id = ex_id,
            start = start_time,
            end = end_time
        )
        df= raw_data.to_pandas()

        #rename columns
        df = df.rename(columns={df.columns[0]:"value"})
        df = df.reset_index()
        df.columns = ["Timestamp", "value"]
        return df

 
    def save_to_csv(self, retrieved_data, file_name = None):
        output_path = file_name or f"{self.pitag}.csv"
        retrieved_data.to_csv(output_path)
        print(f"Saved to {output_path}")

    def push_to_cdf(self, df:pd.DataFrame, ext_id:str = None, unit: str = "unitless"):
        """
        Create and push a time series datapoint from a given DataFrame, to be pushed to CDF.
        Assumes DataFrame has 'Timestamp' and 'value' columns.
        """
        external_id = ext_id or f"{self.ext_id}_{self.agg}"

        if df.empty or "Timestamp" not in df.columns or "value" not in df.columns:
            raise ValueError("Provided DataFrame is invalid or missing required columns.")


        #Check if time-series datapoint already existed, create if not available
        try:
            self.client.time_series.retrieve(external_id=external_id)
            print (f"Time series '{external_id}' already exists.")

        except self.client.exceptions.CogniteNotFoundError:
            self.client.time_series.create({
                "external_id": external_id,
                "name": f"{self.ext_id} ({self.agg})",
                "is_string": False,
                "unit": unit,
                "metadata": {"origin_tag": self.ext_id}
            })
            print(f"✅ Created time series: '{external_id}'")

        #Convert to datapoints
        datapoints = [
            {"timestamp": ts, "value": val}
            for ts, val in zip(df["Timestamp"], df["value"])
            if pd.notna(val)
        ]


        #Push to CDF
        self.client.time_series.data.insert(
            external_id=external_id,
            datapoints=datapoints
        )
        print(f"✅ Inserted {len(datapoints)} datapoints to '{external_id}'")
            
