from cognite.client import CogniteClient
from datetime import datetime
import pandas as pd
 
 
class RetrieveData:
    """Retrieve data of one pi tag with any desidered aggregation method within a time frame. Has method to convert results into pandas dataframe
    """
    def __init__(self, client: CogniteClient):
        self.client = client
        self.pitag = None
 

    def retrieve_data(self, ex_id, start_time_str, end_time_str, agg, interval):
        # Extract tag name for file saving
        raw_tag = ex_id.split(".")[-1]
        self.pitag = raw_tag.replace(".", "_")
    
        # Convert to datetime
        now = datetime.utcnow()
        start_dt = pd.to_datetime(start_time_str)
        end_dt = pd.to_datetime(end_time_str)
    
        # Calculate timedelta differences
        delta_start = now - start_dt
        delta_end = now - end_dt
    
        # Convert timedelta to number of days/hours ago
        start_shift = f"{int(delta_start.total_seconds() // 86400)}d-ago"
        end_shift = f"{int(delta_end.total_seconds() // 86400)}d-ago"
    
        # Retrieve datapoints
        datapoints = self.client.time_series.data.retrieve(
            external_id=ex_id,
            start=start_shift,
            end=end_shift,
            aggregates=agg,
            granularity=interval
        )
    
        df = datapoints.to_pandas()

        #rename columns
        df = df.rename(columns={df.columns[0]:"value"})
        df = df.reset_index()
        df.columns = ["Timestamp", "value"]
        return df

 
    def save_to_csv(self, retrieved_data, file_name = None):
        output_path = file_name or f"{self.pitag}.csv"
        retrieved_data.to_csv(output_path)
        print(f"Saved to {output_path}")
