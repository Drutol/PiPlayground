using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices.WindowsRuntime;
using Windows.Foundation;
using Windows.Foundation.Collections;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Controls.Primitives;
using Windows.UI.Xaml.Data;
using Windows.UI.Xaml.Input;
using Windows.UI.Xaml.Media;
using Windows.UI.Xaml.Navigation;
using Windows.Networking.Sockets;
using Windows.Networking;
using Windows.Storage.Streams;
using System.Text;
using Windows.UI.Core;
using System.Threading;
using Windows.ApplicationModel.Activation;
using Windows.ApplicationModel.DataTransfer;
using Windows.ApplicationModel.DataTransfer.ShareTarget;
using Windows.UI.Popups;
using System.Threading;


namespace PiRemote
{
    public sealed partial class MainPage : Page
    {
        StreamSocket clientSocket = new StreamSocket();
        HostName serverHost;
        public MainPage()
        {
            this.InitializeComponent();

            this.NavigationCacheMode = NavigationCacheMode.Required;
            LinkList.SelectionChanged += LinkList_SelectionChanged;
        }



        protected override void OnNavigatedTo(NavigationEventArgs e)
        {
            SendStringButton.IsEnabled = false;
            Disconnect.IsEnabled = false;
        }

        private async void EstablishConnection(object sender, RoutedEventArgs e)
        {
            serverHost = new HostName(IPBox.Text);
            try
            {
                await clientSocket.ConnectAsync(serverHost, PortBox.Text);
                ConnectButton.IsEnabled = false;
                SendStringButton.IsEnabled = true;
                Disconnect.IsEnabled = true;
                readData();
            }
            catch (Exception) { }
        }



        private async void SendString(string strData,bool getResponse = true)
        {
            try
            {
                byte[] data = Encoding.UTF8.GetBytes(strData);
                IBuffer buffer = data.AsBuffer();

                await clientSocket.OutputStream.WriteAsync(buffer);
            }
            catch (Exception exception)
            {
                if (SocketError.GetStatus(exception.HResult) == SocketErrorStatus.Unknown)
                {
                    StringBox.Text = exception.Message;
                }

            }
          
        }

        private async void readData()
        {
             try
             {
                IBuffer buffer = new byte[1024].AsBuffer();
                await clientSocket.InputStream.ReadAsync(buffer, buffer.Capacity, InputStreamOptions.Partial);
                byte[] result = buffer.ToArray();
                string strReturn = System.Text.Encoding.UTF8.GetString(result, 0, Convert.ToInt32(buffer.Length));
                if(!strReturn.Contains("Links"))
                {
                    StatusLabel.Text = strReturn;
                }
                else
                {
                    ProcessLinks(strReturn);
                }

                readData();
             }
            catch (Exception exception)
            {
                if (SocketError.GetStatus(exception.HResult) == SocketErrorStatus.Unknown)
                {
                    throw;
                }

                StatusLabel.Text = "Receive failed with error: " + exception.Message;
            }
        }

        private void SendStringClick(object sender, RoutedEventArgs e)
        {
            SendString(StringBox.Text);
        }

        private void DisposeConnection(object sender, RoutedEventArgs e)
        {
            SendString("Close Connection",false);
            clientSocket.Dispose();
            clientSocket = new StreamSocket();
            ConnectButton.IsEnabled = true;
            Disconnect.IsEnabled = false;
            SendStringButton.IsEnabled = false;
        }

        private void ButtonPause_Tapped(object sender, TappedRoutedEventArgs e)
        {
            SendString("Pause");
        }

        private void ButtonPlay_Tapped(object sender, TappedRoutedEventArgs e)
        {
            SendString("Play");
        }

        private void ButtonFetchLinks_Click(object sender, RoutedEventArgs e)
        {
            SendString("GimmeLinks");
        }

        private void ProcessLinks(string strLinks)
        {
            LinkList.Items.Clear();
            string[] words = strLinks.Split(';');
            foreach (string word in words)
            {
                if(word != "Links")
                {
                    LinkList.Items.Add(word);
                }
            }



        }

        private void PickTrackAtRandom(object sender, RoutedEventArgs e)
        {
            SendString("random");
        }

        void LinkList_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            SendString(LinkList.SelectedItem.ToString());
        }
   
    }
}
