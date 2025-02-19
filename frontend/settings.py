from frontend.common import *


class Settings(ctk.CTkToplevel):
    """
    A WASTT settings window class with all functionality implemented with its methods.
    """
    def __init__(self, master):
        from config import RUNNING_CONFIG
        super().__init__(master)
        self.root = master
        self.title("WASTT settings")
        self.configure(fg_color=color_bg_br, bg_color=color_bg_br)
        self.protocol("WM_DELETE_WINDOW", self.on_settings_close)
        self.transient(master)
        self.after(250, self.iconbitmap, f"{ASSET_DIR}\\wastt.ico", "")

        settings_width = int(master.winfo_width() * 0.5)
        settings_height = int(master.winfo_height() * 0.9)
        center_window(master, self, settings_width, settings_height)

        self.settings_changed = False
        self.settings_status_label = None

        wrapper = ctk.CTkScrollableFrame(self, fg_color="transparent", bg_color="transparent")
        wrapper.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        label_width = int(settings_width / 5)

        # ================================================
        # General settings isle
        # ================================================
        general_isle = DarkBox(wrapper)
        general_isle.pack(fill=tk.X, padx=10, pady=(10, 5))
        general_header = HeaderTitle(general_isle, "General settings")
        general_header.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 5))
        general_isle_label = Label(
            general_isle,
            text="Changes made in these settings will be applied after restarting the app.",
            justify=tk.LEFT,
            anchor=tk.W
        )
        general_isle_label.pack(side=tk.TOP, fill=tk.X, padx=15, pady=5)
        general_info_button = InfoButton(
            general_isle,
            self,
            "http://localhost:8080/settings.html#general-settings"
        )
        general_info_button.place(relx=1, rely=0, anchor=tk.NE, x=-5, y=15)

        theme_box = Box(general_isle)
        theme_box.pack(fill=tk.X, padx=10, pady=10)
        theme_label = Label(theme_box, text="Theme", width=label_width, anchor=tk.E)
        theme_label.pack(side=tk.LEFT, padx=(10, 5), pady=5)
        self.theme_options = ctk.CTkOptionMenu(
            theme_box,
            values=["System", "Light", "Dark"],
            width=200,
            command=lambda option: self.on_settings_change()
        )
        self.theme_options.set(RUNNING_CONFIG['theme'].capitalize())
        self.theme_options.pack(side=tk.LEFT, padx=(5, 10), pady=5)

        # ================================================
        # Proxy settings isle
        # ================================================
        proxy_isle = DarkBox(wrapper)
        proxy_isle.pack(fill=tk.X, padx=10, pady=5)

        proxy_header = HeaderTitle(proxy_isle, "Proxy settings")
        proxy_header.pack(fill=tk.X, padx=10, pady=(10, 5))
        proxy_info_button = InfoButton(
            proxy_isle,
            self,
            "http://localhost:8080/settings.html#proxy-settings"
        )
        proxy_info_button.place(relx=1, rely=0, anchor=tk.NE, x=-5, y=15)

        proxy_ip_port_box = Box(proxy_isle)
        proxy_ip_port_box.pack(fill=tk.X, padx=10, pady=5)
        proxy_ip_port_label = Label(proxy_ip_port_box, text="Address & Port", width=label_width, anchor=tk.E)
        proxy_ip_port_label.pack(side=tk.LEFT, padx=(10, 5), pady=5)
        self.proxy_ip_input = TextEntry(proxy_ip_port_box, width=200)
        self.proxy_ip_input.bind("<KeyRelease>", self.on_settings_change)
        self.proxy_ip_input.insert(0, RUNNING_CONFIG['proxy_host_address'])
        self.proxy_ip_input.pack(side=tk.LEFT, padx=(5, 0), pady=5)
        proxy_colon_label = Label(proxy_ip_port_box, text=":", anchor=tk.E)
        proxy_colon_label.pack(side=tk.LEFT, padx=0, pady=5)
        self.proxy_port_input = TextEntry(proxy_ip_port_box, width=100)
        self.proxy_port_input.insert(0, RUNNING_CONFIG['proxy_port'])
        self.proxy_port_input.bind("<KeyRelease>", self.on_settings_change)
        self.proxy_port_input.pack(side=tk.LEFT, padx=(0, 10), pady=5)

        proxy_rerun_box = Box(proxy_isle)
        proxy_rerun_box.pack(fill=tk.X, padx=10, pady=(10, 5))
        proxy_rerun_box.grid_columnconfigure(0, minsize=label_width + 10)
        proxy_re_run_label = Label(
            proxy_rerun_box,
            text="Reload proxy",
            width=label_width,
            anchor=tk.E
        )
        proxy_re_run_label.grid(row=0, column=0, sticky=tk.E, padx=(10, 5), pady=5)
        self.proxy_re_run_with_scope_checkbox = ctk.CTkCheckBox(
            proxy_rerun_box,
            text="Retain current scope on reload",
            width=100
        )
        self.proxy_re_run_with_scope_checkbox.grid(row=0, column=1, padx=5, pady=5)
        proxy_re_run_button = ActionButton(
            proxy_rerun_box,
            text="Reload proxy process",
            image=icon_reload,
            command=self.reload_proxy,
            corner_radius=5
        )
        proxy_re_run_button.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        proxy_logs_box = Box(proxy_isle)
        proxy_logs_box.pack(fill=tk.X, padx=10, pady=(10, 5))
        proxy_logs_label = Label(proxy_logs_box, text="Proxy logging", width=label_width, anchor=tk.E)
        proxy_logs_label.pack(side=tk.LEFT, padx=(10, 5), pady=5)
        self.proxy_logs_checkbox = ctk.CTkCheckBox(
            proxy_logs_box,
            text="Log Proxy output to a file.",
            command=self.on_settings_change
        )
        self.proxy_logs_checkbox.pack(side=tk.LEFT, padx=5, pady=5)
        if RUNNING_CONFIG['proxy_logging']:
            self.proxy_logs_checkbox.select()

        proxy_cmd_box = Box(proxy_isle)
        proxy_cmd_box.pack(fill=tk.X, padx=10, pady=10)
        proxy_cmd_label = Label(proxy_cmd_box, text="Proxy terminal", width=label_width, anchor=tk.E)
        proxy_cmd_label.pack(side=tk.LEFT, padx=(10, 5), pady=5)
        self.proxy_cmd_checkbox = ctk.CTkCheckBox(
            proxy_cmd_box,
            text="Show Proxy output in terminal window.",
            command=self.on_settings_change
        )
        if RUNNING_CONFIG['proxy_console']:
            self.proxy_cmd_checkbox.select()
        self.proxy_cmd_checkbox.pack(side=tk.LEFT, padx=5, pady=(5, 10))

        # ================================================
        # Browser settings isle
        # ================================================
        browser_isle = DarkBox(wrapper)
        browser_isle.pack(fill=tk.X, padx=10, pady=5)
        browser_settings = HeaderTitle(browser_isle, "Browser settings")
        browser_settings.pack(fill=tk.X, padx=10, pady=(10, 5))
        browser_info_button = InfoButton(
            browser_isle,
            self,
            "http://localhost:8080/settings.html#browser-settings"
        )
        browser_info_button.place(relx=1, rely=0, anchor=tk.NE, x=-5, y=15)

        broswer_type_box = Box(browser_isle)
        broswer_type_box.pack(fill=tk.X, padx=10, pady=5)
        broswer_type_box_label = Label(broswer_type_box, text="Browser type", width=label_width, anchor=tk.E)
        broswer_type_box_label.pack(side=tk.LEFT, padx=(10, 5), pady=5)
        self.broswer_type_options = ctk.CTkOptionMenu(
            broswer_type_box,
            values=["Chrome", "Edge", "Firefox"],
            width=200,
            command=lambda option: self.on_settings_change()
        )
        self.broswer_type_options.set(RUNNING_CONFIG['browser_type'].capitalize())
        self.broswer_type_options.pack(side=tk.LEFT, padx=(5, 10), pady=5)

        broswer_disable_info_box = Box(browser_isle)
        broswer_disable_info_box.pack(fill=tk.X, padx=10, pady=5)
        broswer_disable_info_label = Label(broswer_disable_info_box, text="Disable infobars", width=label_width, anchor=tk.E)
        broswer_disable_info_label.pack(side=tk.LEFT, padx=(10, 5), pady=5)
        self.broswer_disable_info_checkbox = ctk.CTkCheckBox(
            broswer_disable_info_box,
            text="Disable all infobars and notifications in the browser.",
            command=self.on_settings_change
        )
        if RUNNING_CONFIG['browser_disable_infobars']:
            self.broswer_disable_info_checkbox.select()
        self.broswer_disable_info_checkbox.pack(side=tk.LEFT, padx=5, pady=5)

        broswer_disable_cert_errors_box = Box(browser_isle)
        broswer_disable_cert_errors_box.pack(fill=tk.X, padx=10, pady=(5, 10))
        broswer_disable_cert_errors_label = Label(broswer_disable_cert_errors_box, text="Disable certifacte errors", width=label_width, anchor=tk.E)
        broswer_disable_cert_errors_label.pack(side=tk.LEFT, padx=(10, 5), pady=5)
        self.broswer_disable_cert_errors_checkbox = ctk.CTkCheckBox(
            broswer_disable_cert_errors_box,
            text="Disable all certicate errors and warnings in the browser.",
            command=self.on_settings_change
        )
        if RUNNING_CONFIG['browser_disable_cert_errors']:
            self.broswer_disable_cert_errors_checkbox.select()
        self.broswer_disable_cert_errors_checkbox.pack(side=tk.LEFT, padx=5, pady=(5, 10))

        # ================================================
        # Logs settings isle
        # ================================================
        logs_isle = DarkBox(wrapper)
        logs_isle.pack(fill=tk.X, padx=10, pady=5)
        logs_settings = HeaderTitle(logs_isle, "Logs settings")
        logs_settings.pack(fill=tk.X, padx=10, pady=5)
        logs_info_button = InfoButton(
            logs_isle,
            self,
            "http://localhost:8080/settings.html#logs-settings"
        )
        logs_info_button.place(relx=1, rely=0, anchor=tk.NE, x=-5, y=15)

        logs_location_box = Box(logs_isle)
        logs_location_box.pack(fill=tk.X, padx=10, pady=5)
        logs_location_label = Label(logs_location_box, text="Logs locations", width=label_width, anchor=tk.E)
        logs_location_label.pack(side=tk.LEFT, padx=(10, 5), pady=5)
        self.logs_location_input = TextEntry(
            logs_location_box,
            width=450
        )
        self.logs_location_input.insert(0, RUNNING_CONFIG['logs_location'])
        self.logs_location_input.bind("<KeyRelease>", self.on_settings_change)
        self.logs_location_input.pack(side=tk.LEFT, padx=5, pady=(5, 10))
        self.logs_location_button = ActionButton(
            logs_location_box,
            text="",
            image=icon_folder,
            width=25,
            corner_radius=5,
            command=self.select_log_file_dir
        )
        self.logs_location_button.pack(side=tk.LEFT, padx=5, pady=(5, 10))

        logs_http_traffic_box = Box(logs_isle)
        logs_http_traffic_box.pack(fill=tk.X, padx=10, pady=5)
        logs_http_traffic_label = Label(logs_http_traffic_box, text="Log HTTP traffic", width=label_width, anchor=tk.E)
        logs_http_traffic_label.pack(side=tk.LEFT, padx=(10, 5), pady=5)
        self.logs_http_traffic_checkbox = ctk.CTkCheckBox(
            logs_http_traffic_box,
            text="Log whole HTTP traffic flow - requests and responses.",
            command=self.on_settings_change
        )
        if RUNNING_CONFIG['log_http_traffic_flow']:
            self.logs_http_traffic_checkbox.select()
        self.logs_http_traffic_checkbox.pack(side=tk.LEFT, padx=5, pady=5)

        logs_intercepted_requests_box = Box(logs_isle)
        logs_intercepted_requests_box.pack(fill=tk.X, padx=10, pady=(5, 15))
        logs_intercepted_requests_label = Label(logs_intercepted_requests_box, text="Log intercepted requests", width=label_width, anchor=tk.E)
        logs_intercepted_requests_label.pack(side=tk.LEFT, padx=(10, 5), pady=5)
        self.logs_intercepted_requests_checkbox = ctk.CTkCheckBox(
            logs_intercepted_requests_box,
            text="Log requests intercepted by Web Request Interceptor.",
            command=self.on_settings_change
        )
        if RUNNING_CONFIG['log_intercepted_requests']:
            self.logs_intercepted_requests_checkbox.select()
        self.logs_intercepted_requests_checkbox.pack(side=tk.LEFT, padx=5, pady=5)

        # ================================================
        # Debug settings isle
        # ================================================
        debug_isle = DarkBox(wrapper)
        debug_isle.pack(fill=tk.X, padx=10, pady=5)
        debug_settings = HeaderTitle(debug_isle, "Debug settings")
        debug_settings.pack(fill=tk.X, padx=10, pady=(10, 5))
        debug_isle_label = Label(
            debug_isle,
            text="Changes made in these settings will be applied after restarting the app.",
            justify=tk.LEFT,
            anchor=tk.W
        )
        debug_isle_label.pack(side=tk.TOP, fill=tk.X, padx=15, pady=5)
        debug_info_button = InfoButton(
            debug_isle,
            self,
            "http://localhost:8080/settings.html#debug-settings"
        )
        debug_info_button.place(relx=1, rely=0, anchor=tk.NE, x=-5, y=15)

        debug_mode_box = Box(debug_isle)
        debug_mode_box.pack(fill=tk.X, padx=10, pady=5)
        debug_mode_label = Label(debug_mode_box, text="Debug mode", width=label_width, anchor=tk.E)
        debug_mode_label.pack(side=tk.LEFT, padx=(10, 5), pady=5)
        self.debug_mode_checkbox = ctk.CTkCheckBox(
            debug_mode_box,
            text="Show all application operations in the Python's output.",
            command=self.on_settings_change
        )
        if RUNNING_CONFIG['debug_mode']:
            self.debug_mode_checkbox.select()
        self.debug_mode_checkbox.pack(side=tk.LEFT, padx=5, pady=(5, 10))

        debug_running_conf_box = Box(debug_isle)
        debug_running_conf_box.pack(fill=tk.X, padx=10, pady=(5, 10))
        debug_running_conf_label = Label(debug_running_conf_box, text="Show running conf", width=label_width, anchor=tk.E)
        debug_running_conf_label.pack(side=tk.LEFT, padx=(10, 5), pady=5)
        self.debug_running_conf_checkbox = ctk.CTkCheckBox(
            debug_running_conf_box,
            text="Show currently running configuration on app's start up in the Python's output.",
            command=self.on_settings_change
        )
        if RUNNING_CONFIG['debug_show_running_config']:
            self.debug_running_conf_checkbox.select()
        self.debug_running_conf_checkbox.pack(side=tk.LEFT, padx=5, pady=(5, 10))

        # ================================================
        # Bottom Bar
        # ================================================
        bottom_bar = ctk.CTkFrame(
            self,
            fg_color=color_bg,
            bg_color="transparent",
            corner_radius=10
        )
        bottom_bar.pack(fill=tk.X, padx=(15, 25), pady=(5, 20))
        self.settings_status_label = ctk.CTkLabel(bottom_bar, text="Settings unchanged.")
        self.settings_status_label.pack(side=tk.LEFT, padx=10, pady=10)
        self.save_button = ActionButton(
            bottom_bar,
            text="Save",
            command=self.read_new_settings,
            state=tk.DISABLED
        )
        self.cancel_button = ActionButton(
            bottom_bar,
            text="Cancel",
            command=self.destroy,
            fg_color=color_acc3,
            hover_color=color_acc4
        )
        self.cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)
        self.save_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def on_settings_change(self, _event=None) -> None:
        """
        Marks settings as changed, updates the settings status label text, and enables the save button.
        """
        self.settings_status_label.configure(text="Settings has been changed. Save to apply changes.")
        self.save_button.configure(state=tk.NORMAL)
        self.settings_changed = True

    def on_settings_close(self) -> None:
        """
        Handles the closing procedure of an application settings window.
        This method checks for unsaved changes and prompts the user with options to either save,
        discard, or go back to the settings. If no changes are detected, the settings window
        closes without additional prompts.
        """
        if self.settings_changed:
            confirm = ConfirmDialog(
                self.root,
                self,
                "You have unsaved changes. Do you want to save them?",
                "Save changes?",
                "Save new settings",
                lambda: (self.read_new_settings(), confirm.destroy()),
                "Discard new settings",
                lambda: (self.destroy_window(), confirm.destroy()),
                "Go back",
                lambda: confirm.destroy(),
                width=550
            )
        else:
            self.destroy_window()

    def destroy_window(self) -> None:
        """
        Destroy a settings window.

        This method is responsible for destroying the current settings window and
        removes its reference in the parent `root` object to allow the system to
        clear up resources.
        """
        self.root.settings_window = None
        self.destroy()

    def reload_proxy(self, retain_scope: bool = False) -> None:
        """
        Reloads the proxy configuration and optionally retains the current scope.
        Utilizes the given state of scope retention to determine the scope behavior
        during the proxy reload process. Debug messages provide feedback on the
        reload process and the applied scope status.
        """
        if retain_scope or self.proxy_re_run_with_scope_checkbox.get():
            current_scope = self.root.proxy.current_scope
            self.root.proxy.run_mitmdump(current_scope)
            dprint("[DEBUG] Reloading with scope.")
        else:
            self.root.proxy.run_mitmdump()
            dprint("[DEBUG] Reloading without scope.")

    def select_log_file_dir(self) -> None:
        """
        Selects a directory for log files and updates the input field with the selected path.
        Triggers settings change callback after directory selection.
        """
        self.on_settings_change()
        file_path = filedialog.askdirectory(
            initialdir=RUNNING_CONFIG['logs_location'],
            title="Select main directory for logs"
        )
        if file_path:
            self.logs_location_input.delete(0, tk.END)
            self.logs_location_input.insert(0, file_path)

    def read_new_settings(self) -> None:
        """
        Reads and processes new settings for the application, updates the configuration, and determines if
        restarts are needed for proxy or browser components. If any restart is necessary, prompts the user
        for confirmation before applying changes.
        """
        new_config = {
            "theme": self.theme_options.get().lower().strip(),
            "proxy_host_address": self.proxy_ip_input.get(),
            "proxy_port": self.proxy_port_input.get(),
            "proxy_logging": self.proxy_logs_checkbox.get(),
            "proxy_console": self.proxy_cmd_checkbox.get(),
            "browser_type": self.broswer_type_options.get().lower(),
            "browser_disable_infobars": self.broswer_disable_info_checkbox.get(),
            "browser_disable_cert_errors": self.broswer_disable_cert_errors_checkbox.get(),
            "logs_location": self.logs_location_input.get(),
            "log_http_traffic_flow": self.logs_http_traffic_checkbox.get(),
            "log_intercepted_requests": self.logs_intercepted_requests_checkbox.get(),
            "debug_mode": self.debug_mode_checkbox.get(),
            "debug_show_running_config": self.debug_running_conf_checkbox.get()
        }

        dprint("================================================\n"
               "[DEBUG] New config:")
        for key, value in new_config.items():
            dprint(f"\t{key}: {value}")
        dprint("================================================")

        proxy_restart = (new_config["proxy_host_address"] != RUNNING_CONFIG["proxy_host_address"] or
                         new_config["proxy_port"] != RUNNING_CONFIG["proxy_port"] or
                         new_config["proxy_logging"] != RUNNING_CONFIG["proxy_logging"] or
                         new_config["proxy_console"] != RUNNING_CONFIG["proxy_console"])
        dprint(f"[DEBUG] Proxy restart needed: {proxy_restart}")
        browser_restart = (new_config["browser_type"] != RUNNING_CONFIG["browser_type"] or
                           new_config["browser_disable_infobars"] != RUNNING_CONFIG["browser_disable_infobars"] or
                           new_config["browser_disable_cert_errors"] != RUNNING_CONFIG["browser_disable_cert_errors"])
        dprint(f"[DEBUG] Browser restart needed: {browser_restart}")

        if proxy_restart and browser_restart:
            confirm = ConfirmDialog(
                self.root,
                self,
                "To apply some changes browser and proxy process will be restarted.",
                "Proxy and browser restart needed",
                "Ok",
                lambda: (self.save_settings(new_config, reload_proxy=proxy_restart, reload_browser=browser_restart), confirm.destroy()),
            )
        elif proxy_restart:
            confirm = ConfirmDialog(
                self.root,
                self,
                "To apply some changes mitmdump proxy process will be restarted.",
                "Proxy restart needed",
                "Ok",
                lambda: (self.save_settings(new_config, reload_proxy=proxy_restart, reload_browser=browser_restart), confirm.destroy()),
            )
        elif browser_restart:
            confirm = ConfirmDialog(
                self.root,
                self,
                "To apply some changes the web browser process will be restarted.",
                "Browser restart needed",
                lambda: (self.save_settings(new_config, reload_proxy=proxy_restart, reload_browser=browser_restart), confirm.destroy()),
            )
        else:
            self.save_settings(new_config)

    def save_settings(self, new_config: dict, reload_proxy: bool = False, reload_browser: bool = False) -> None:
        """
        Saves the provided configurations and optionally reloads proxy and/or browser.

        This method updates the application settings by saving the new configuration
        provided through its arguments. If specified, it also reloads the network
        proxy settings and reinitializes the browser state. After performing these
        actions, the method ensures that any related settings window is destroyed.

        Parameters:
            new_config (dict): A dictionary containing the new configuration settings.
            reload_proxy (bool): Indicates whether to reload the proxy settings.
            reload_browser (bool): Indicates whether to reload and reinitialize the browser.
        """
        dprint("[DEBUG] Saving settings.")
        from config import save_config, update_config
        update_config(new_config)
        save_config(new_config)
        if reload_proxy:
            dprint("[DEBUG] Reloading proxy.")
            self.reload_proxy(retain_scope=True)
        if reload_browser:
            if self.root.browser_opened:
                dprint("[DEBUG] Reopening browser.")
                if self.root.browser is not None:
                    self.root.browser.quit()
                self.root.browser = None
                self.root.start_browser_thread()
            else:
                self.root.browser = None

        self.destroy_window()
