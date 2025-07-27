using Microsoft.VisualStudio.Shell;
using Microsoft.VisualStudio.Shell.Interop;
using System;
using System.ComponentModel.Design;
using System.Runtime.InteropServices;
using System.Threading;
using Task = System.Threading.Tasks.Task;

namespace KimiK2Coder
{
    /// <summary>
    /// Kimi K2 Coder Package - Main extension entry point
    /// </summary>
    [PackageRegistration(UseManagedResourcesOnly = true, AllowsBackgroundLoading = true)]
    [Guid(PackageGuids.KimiK2CoderPackageString)]
    [ProvideMenuResource("Menus.ctmenu", 1)]
    [ProvideOptionPage(typeof(KimiK2OptionsPage), "Kimi K2 Coder", "General", 0, 0, true)]
    [ProvideToolWindow(typeof(KimiK2ToolWindow))]
    public sealed class KimiK2CoderPackage : AsyncPackage
    {
        /// <summary>
        /// Initialization of the package; this method is called right after the package is sited
        /// </summary>
        /// <param name="cancellationToken">A cancellation token to monitor for initialization cancellation</param>
        /// <param name="progress">A provider for progress updates</param>
        /// <returns>A task representing the async work of package initialization</returns>
        protected override async Task InitializeAsync(CancellationToken cancellationToken, IProgress<ServiceProgressData> progress)
        {
            // When initialized asynchronously, the current thread may be a background thread at this point.
            // Do any initialization that requires the UI thread after switching to the UI thread.
            await this.JoinableTaskFactory.SwitchToMainThreadAsync(cancellationToken);

            // Initialize menu commands
            await KimiK2Commands.InitializeAsync(this);
            
            // Initialize the tool window
            var toolWindowCommand = new ToolWindowCommand(this);
            toolWindowCommand.Initialize();
        }

        /// <summary>
        /// Gets the Kimi K2 service instance
        /// </summary>
        public KimiK2Service GetKimiService()
        {
            return GetService(typeof(KimiK2Service)) as KimiK2Service;
        }
    }

    /// <summary>
    /// Package GUIDs
    /// </summary>
    public static class PackageGuids
    {
        public const string KimiK2CoderPackageString = "12345678-1234-1234-1234-123456789012";
        public static readonly Guid KimiK2CoderPackage = new Guid(KimiK2CoderPackageString);
    }
}