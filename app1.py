
import streamlit as st
import pandas as pd
import datetime
import base64
import Preprocessing
import pickle

PAGE_CONFIG = {"page_title": "Delay_prediction.io", "page_icon": ":smiley:", "layout": "centered"}
st.beta_set_page_config(**PAGE_CONFIG)

def Source_Details(df_airport):
    # Input Options
    Source_dict = {'Select':'Default','Newark Liberty Intl': 'EWR', 'La Guardia': 'LGA', 'John F Kennedy Intl': 'JFK'}
    # Set Source(Airport Name)
    Source_Name = st.sidebar.selectbox('Source', list(Source_dict.keys()))
    Source_Code = Source_dict[Source_Name]
    if Source_Code== "Default":
        return Source_Code,Source_Name, {}
    # Get Lat, Lon, and Alt for Source
    Source_location = df_airport.loc[df_airport.faa == Source_Code][["lat", "lon", "alt"]]
    Source_location = list(Source_location.T.to_dict().values())[0]
    return Source_Code,Source_Name,Source_location
def Destination(df_airport,df_flights,Source_Code):

    temp = pd.merge(df_airport[["faa", "name", "lat", "lon", "alt"]], df_flights[["origin", "dest"]],
                    left_on='faa', right_on='dest', how="inner")

    if Source_Code=="Default":
        st.sidebar.selectbox("Destination", ["Select Source First"])
        return  "","", {}
    Destination_Info = temp[temp.origin ==Source_Code].drop_duplicates()
    # temp1 = temp1.drop_duplicates()
    Destination_Info = Destination_Info.set_index('name').T

    #Get Lat, Lon and Alt
    Dest_dict = Destination_Info.iloc[0].to_dict()
    Dest_info = Destination_Info.iloc[1:4].to_dict()  # Destination Lat lon alt

    # Set Value of Destination
    Destination = list(set(Dest_dict.keys()))
    Destination_Name = st.sidebar.selectbox("Destination", Destination)
    Destination_Code = Dest_dict[Destination_Name]

    Destination_location = Dest_info[Destination_Name]
    # print("Destination_location", Dest_info)
    return Destination_Code,Destination_Name,Destination_location
def Find_Flight(df_flights,date,Source_Code,Destination_Code): #Code Source and Deatination
    if Source_Code=="Default":
        st.sidebar.selectbox("Flights",["Empty"])
        return  pd.DataFrame(),""
    date = pd.Series(date)
    # Find Flight For Specific Date (Source -> Destination )
    Flights=df_flights.loc[(df_flights.month==date[0].month)&(df_flights.day==date[0].day)&
                           (df_flights.origin==Source_Code) & (df_flights.dest==Destination_Code)]
    Flight_display={}
    ## To Create Sidebar
    for i,j in zip(Flights["manufacturer"],Flights["tailnum"]):
        Flight_display[str(i+"-"+j)]=[j]
    # Set Value of Flight list

    Flights1=st.sidebar.selectbox("Flights",list(Flight_display.keys()))

    if Flights1!=None:
        ## Featching data of flight for prediction
        One_Flight=Flights.loc[(Flights.tailnum==Flight_display[Flights1][0])]

        if (One_Flight.shape[0] == 1):
            One_Flight.reset_index(drop=True, inplace=True)

            return One_Flight,Flights1
        else:
            st.subheader("No Flight Found")
            return pd.DataFrame(),""

    else:
        st.subheader("No Flight Found")
        return pd.DataFrame(),""
def Prediction(Model,One_Flight, Source_Location, Destination_Location):
    Predict_Input={}
    if len(Predict_Input.values())==0:
        st.subheader("Loading Prediction...")
    Predict_Input = Preprocessing.Preprocessing_df(One_Flight, Source_Location, Destination_Location)
    result = Model.predict([list(Predict_Input.values())])
    result1 = Model.predict_proba([list(Predict_Input.values())])

    st.header("Prediction : " + "The flight will not be a delay. "
                 if result == 0 else "The flight will be a delay.")
    st.header("Probability : %.2f" % (result1[0][0] * 100)+"%" if result == 0 else (result1[0][1] * 100)+"%")
def main(df_flights, df_airport,Model):

    st.title("Welcome To, Flight Delay Prediction")

    Source_Code,Source_Name,Source_location=Source_Details(df_airport)
    Destination_Code, Destination_Name, Destination_location=Destination(df_airport,df_flights,Source_Code)
    date = st.sidebar.date_input('Date', datetime.datetime.now())
    One_Flight,Flight_Name=Find_Flight(df_flights,date,Source_Code,Destination_Code)
    Predict = st.sidebar.button("Predict Delay")
    st.subheader(f"Date :  {date}")
    if Source_Code!="Default":
        st.subheader("From : " + Source_Name + " - "+ Source_Code)
        st.subheader("To : " + Destination_Name+" - "+Destination_Code)


        if Predict==True:
            if One_Flight.shape[0]!=1:
                st.subheader("No Flight Found")
                return
            st.subheader("Distance : " + str(One_Flight.distance[0])+" km")
            st.subheader("Flight Name : " + Flight_Name)
            st.subheader("Flight Capacity : " + str(One_Flight.seats[0]))
            # st.subheader("Airplane Type : " + str(One_Flight.type[0]))
            # st.subheader("Manufacturer Name : " + str(One_Flight.manufacturer[0]))
            # st.subheader("Model Name : " + str(One_Flight.model[0]))

            Prediction(Model,One_Flight, Source_location, Destination_location)
    else:
        st.subheader("Please Select Location , Date and Flight...")






if __name__ == '__main__':
    @st.cache(allow_output_mutation=True)
    def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()


    def set_png_as_page_bg(png_file):
        bin_str = get_base64_of_bin_file(png_file)
        page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    
    
    </style>
    
    ''' % bin_str

        st.markdown(page_bg_img, unsafe_allow_html=True)
        return


    set_png_as_page_bg('Background.jpg')

    @st.cache(suppress_st_warning=False)
    def load_dataset():
        filename = 'Logistic_model_V1.sav'
        Model = pickle.load(open('Models/'+filename, 'rb'))
        # data = df_airport=pd.read_csv("/content/drive/My Drive/ML/Datasets/Nyc_Airline/ready_data_15.csv")
        df_flights = pd.read_csv("modified_flight.csv")
        # df_weather = pd.read_csv("modified_weather.csv")
        df_airport = pd.read_csv("nyc_airports.csv")
        print("loaded")
        return df_flights,  df_airport,Model


    st.markdown('<style>h1{color: black;}</style>', unsafe_allow_html=True)

    st.markdown('<style>h2{color: black;font-size: 24px;}</style>', unsafe_allow_html=True)#font-weight: 1000;
    # st.markdown('<style>buttons{background-color: #f44336;}</style>')
    # st.markdown('<style>h1{color: black;}</style>', unsafe_allow_html=True)

    df_flights, df_airport,Model = load_dataset()
    main(df_flights, df_airport,Model)