using PiRemote.Common;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices.WindowsRuntime;
using Windows.ApplicationModel.Activation;
using Windows.ApplicationModel.DataTransfer.ShareTarget;
using Windows.Foundation;
using Windows.Foundation.Collections;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Controls.Primitives;
using Windows.UI.Xaml.Data;
using Windows.UI.Xaml.Input;
using Windows.UI.Xaml.Media;
using Windows.UI.Xaml.Media.Imaging;
using Windows.UI.Xaml.Navigation;

// The Share Target Contract item template is documented at http://go.microsoft.com/fwlink/?LinkID=390556

namespace PiRemote
{
    /// <summary>
    /// This page allows other applications to share content through this application.
    /// </summary>
    public sealed partial class ShareTarget1 : Page
    {
        /// <summary>
        /// Provides a channel to communicate with Windows about the sharing operation.
        /// </summary>
        private ShareOperation shareOperation;
        private ObservableDictionary defaultViewModel = new ObservableDictionary();

        public ShareTarget1()
        {
            this.InitializeComponent();
        }

        /// <summary>
        /// Gets the view model for this <see cref="Page"/>.
        /// This can be changed to a strongly typed view model.
        /// </summary>
        public ObservableDictionary DefaultViewModel
        {
            get { return this.defaultViewModel; }
        }

        /// <summary>
        /// Invoked when another application wants to share content through this application.
        /// </summary>
        /// <param name="e">Activation data used to coordinate the process with Windows.</param>
        public async void Activate(ShareTargetActivatedEventArgs e)
        {
            this.shareOperation = e.ShareOperation;

            // Communicate metadata about the shared content through the view model
            var shareProperties = this.shareOperation.Data.Properties;
            var thumbnailImage = new BitmapImage();
            this.DefaultViewModel["Title"] = shareProperties.Title;
            this.DefaultViewModel["Description"] = shareProperties.Description;
            this.DefaultViewModel["Image"] = thumbnailImage;
            this.DefaultViewModel["Sharing"] = false;
            this.DefaultViewModel["ShowImage"] = false;
            this.DefaultViewModel["Comment"] = string.Empty;
            this.DefaultViewModel["Placeholder"] = "Add a comment";
            this.DefaultViewModel["SupportsComment"] = true;
            Window.Current.Content = this;
            Window.Current.Activate();

            // Update the shared content's thumbnail image in the background
            if (shareProperties.Thumbnail != null)
            {
                var stream = await shareProperties.Thumbnail.OpenReadAsync();
                thumbnailImage.SetSource(stream);
                this.DefaultViewModel["ShowImage"] = true;
            }
        }

        /// <summary>
        /// Invoked when the user clicks the Share button.
        /// </summary>
        /// <param name="sender">Instance of Button used to initiate sharing.</param>
        /// <param name="e">Event data describing how the button was clicked.</param>
        private void ShareButton_Click(object sender, RoutedEventArgs e)
        {
            this.DefaultViewModel["Sharing"] = true;

            // TODO: Perform work appropriate to your sharing scenario using
            //       this._shareOperation.Data, typically with additional information captured
            //       through custom user interface elements added to this page such as 
            //       this.DefaultViewModel["Comment"]

            this.shareOperation.ReportCompleted();
        }
    }
}
