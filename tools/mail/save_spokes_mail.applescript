-- Apple Mail rule action: save each matching message's raw source as .eml
-- into ~/spokes_sources/mail-inbox/ so the daily Spokes job can process it.
using terms from application "Mail"
	on perform mail action with messages theMessages for rule theRule
		set outDir to (POSIX path of (path to home folder)) & "spokes_sources/mail-inbox/"
		do shell script "mkdir -p " & quoted form of outDir
		repeat with m in theMessages
			try
				tell application "Mail"
					set mid to message id of m
					set src to source of m
				end tell
				set fname to do shell script "printf %s " & quoted form of mid & " | shasum | cut -c1-16"
				set fpath to outDir & fname & ".eml"
				set fh to open for access (POSIX file fpath) with write permission
				set eof fh to 0
				write src to fh as «class utf8»
				close access fh
			on error
				try
					close access (POSIX file fpath)
				end try
			end try
		end repeat
	end perform mail action with messages
end using terms from
