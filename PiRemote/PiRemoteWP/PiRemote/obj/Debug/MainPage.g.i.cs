﻿

#pragma checksum "C:\Users\Mordonus\documents\visual studio 2013\Projects\PiRemote\PiRemote\MainPage.xaml" "{406ea660-64cf-4c82-b6f0-42d48172a799}" "592ED357ABE5B0BA5CF7B40C32AE8F6F"
//------------------------------------------------------------------------------
// <auto-generated>
//     This code was generated by a tool.
//
//     Changes to this file may cause incorrect behavior and will be lost if
//     the code is regenerated.
// </auto-generated>
//------------------------------------------------------------------------------

namespace PiRemote
{
    partial class MainPage : global::Windows.UI.Xaml.Controls.Page
    {
        [global::System.CodeDom.Compiler.GeneratedCodeAttribute("Microsoft.Windows.UI.Xaml.Build.Tasks"," 4.0.0.0")]
        private global::Windows.UI.Xaml.Controls.Image PiLogo; 
        [global::System.CodeDom.Compiler.GeneratedCodeAttribute("Microsoft.Windows.UI.Xaml.Build.Tasks"," 4.0.0.0")]
        private global::Windows.UI.Xaml.Controls.TextBlock Title; 
        [global::System.CodeDom.Compiler.GeneratedCodeAttribute("Microsoft.Windows.UI.Xaml.Build.Tasks"," 4.0.0.0")]
        private global::Windows.UI.Xaml.Controls.ListView LinkList; 
        [global::System.CodeDom.Compiler.GeneratedCodeAttribute("Microsoft.Windows.UI.Xaml.Build.Tasks"," 4.0.0.0")]
        private global::Windows.UI.Xaml.Controls.Button ButtonFetchLinks; 
        [global::System.CodeDom.Compiler.GeneratedCodeAttribute("Microsoft.Windows.UI.Xaml.Build.Tasks"," 4.0.0.0")]
        private global::Windows.UI.Xaml.Controls.TextBox IPBox; 
        [global::System.CodeDom.Compiler.GeneratedCodeAttribute("Microsoft.Windows.UI.Xaml.Build.Tasks"," 4.0.0.0")]
        private global::Windows.UI.Xaml.Controls.Button ConnectButton; 
        [global::System.CodeDom.Compiler.GeneratedCodeAttribute("Microsoft.Windows.UI.Xaml.Build.Tasks"," 4.0.0.0")]
        private global::Windows.UI.Xaml.Controls.Button ButtonRandom; 
        [global::System.CodeDom.Compiler.GeneratedCodeAttribute("Microsoft.Windows.UI.Xaml.Build.Tasks"," 4.0.0.0")]
        private global::Windows.UI.Xaml.Controls.Button SendStringButton; 
        [global::System.CodeDom.Compiler.GeneratedCodeAttribute("Microsoft.Windows.UI.Xaml.Build.Tasks"," 4.0.0.0")]
        private global::Windows.UI.Xaml.Controls.TextBox StringBox; 
        [global::System.CodeDom.Compiler.GeneratedCodeAttribute("Microsoft.Windows.UI.Xaml.Build.Tasks"," 4.0.0.0")]
        private global::Windows.UI.Xaml.Controls.TextBox PortBox; 
        [global::System.CodeDom.Compiler.GeneratedCodeAttribute("Microsoft.Windows.UI.Xaml.Build.Tasks"," 4.0.0.0")]
        private global::Windows.UI.Xaml.Controls.Button Disconnect; 
        [global::System.CodeDom.Compiler.GeneratedCodeAttribute("Microsoft.Windows.UI.Xaml.Build.Tasks"," 4.0.0.0")]
        private global::Windows.UI.Xaml.Controls.TextBlock StatusLabel; 
        [global::System.CodeDom.Compiler.GeneratedCodeAttribute("Microsoft.Windows.UI.Xaml.Build.Tasks"," 4.0.0.0")]
        private global::Windows.UI.Xaml.Controls.Button ButtonPause; 
        [global::System.CodeDom.Compiler.GeneratedCodeAttribute("Microsoft.Windows.UI.Xaml.Build.Tasks"," 4.0.0.0")]
        private global::Windows.UI.Xaml.Controls.Button ButtonPlay; 
        [global::System.CodeDom.Compiler.GeneratedCodeAttribute("Microsoft.Windows.UI.Xaml.Build.Tasks"," 4.0.0.0")]
        private bool _contentLoaded;

        [global::System.CodeDom.Compiler.GeneratedCodeAttribute("Microsoft.Windows.UI.Xaml.Build.Tasks"," 4.0.0.0")]
        [global::System.Diagnostics.DebuggerNonUserCodeAttribute()]
        public void InitializeComponent()
        {
            if (_contentLoaded)
                return;

            _contentLoaded = true;
            global::Windows.UI.Xaml.Application.LoadComponent(this, new global::System.Uri("ms-appx:///MainPage.xaml"), global::Windows.UI.Xaml.Controls.Primitives.ComponentResourceLocation.Application);
 
            PiLogo = (global::Windows.UI.Xaml.Controls.Image)this.FindName("PiLogo");
            Title = (global::Windows.UI.Xaml.Controls.TextBlock)this.FindName("Title");
            LinkList = (global::Windows.UI.Xaml.Controls.ListView)this.FindName("LinkList");
            ButtonFetchLinks = (global::Windows.UI.Xaml.Controls.Button)this.FindName("ButtonFetchLinks");
            IPBox = (global::Windows.UI.Xaml.Controls.TextBox)this.FindName("IPBox");
            ConnectButton = (global::Windows.UI.Xaml.Controls.Button)this.FindName("ConnectButton");
            ButtonRandom = (global::Windows.UI.Xaml.Controls.Button)this.FindName("ButtonRandom");
            SendStringButton = (global::Windows.UI.Xaml.Controls.Button)this.FindName("SendStringButton");
            StringBox = (global::Windows.UI.Xaml.Controls.TextBox)this.FindName("StringBox");
            PortBox = (global::Windows.UI.Xaml.Controls.TextBox)this.FindName("PortBox");
            Disconnect = (global::Windows.UI.Xaml.Controls.Button)this.FindName("Disconnect");
            StatusLabel = (global::Windows.UI.Xaml.Controls.TextBlock)this.FindName("StatusLabel");
            ButtonPause = (global::Windows.UI.Xaml.Controls.Button)this.FindName("ButtonPause");
            ButtonPlay = (global::Windows.UI.Xaml.Controls.Button)this.FindName("ButtonPlay");
        }
    }
}



