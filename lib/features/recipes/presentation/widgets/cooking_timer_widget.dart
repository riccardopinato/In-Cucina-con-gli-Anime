import 'dart:async';

import 'package:flutter/material.dart';

import '../../../../l10n/app_localizations.dart';

class CookingTimerWidget extends StatefulWidget {
  const CookingTimerWidget({
    super.key,
    required this.minutes,
  });

  final int minutes;

  @override
  State<CookingTimerWidget> createState() => _CookingTimerWidgetState();
}

class _CookingTimerWidgetState extends State<CookingTimerWidget> {
  Timer? _timer;
  late int _totalSeconds;
  late int _remainingSeconds;
  bool _running = false;

  @override
  void initState() {
    super.initState();
    _resetValues();
  }

  @override
  void didUpdateWidget(covariant CookingTimerWidget oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.minutes != widget.minutes) {
      _timer?.cancel();
      _resetValues();
    }
  }

  void _resetValues() {
    _totalSeconds = widget.minutes * 60;
    _remainingSeconds = _totalSeconds;
    _running = false;
  }

  void _start() {
    if (_remainingSeconds <= 0 || _running) return;

    setState(() => _running = true);
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (!mounted) {
        timer.cancel();
        return;
      }

      if (_remainingSeconds <= 1) {
        timer.cancel();
        setState(() {
          _remainingSeconds = 0;
          _running = false;
        });
        _showFinishedDialog();
        return;
      }

      setState(() => _remainingSeconds -= 1);
    });
  }

  void _pause() {
    _timer?.cancel();
    setState(() => _running = false);
  }

  void _reset() {
    _timer?.cancel();
    setState(_resetValues);
  }

  Future<void> _showFinishedDialog() async {
    final l10n = AppLocalizations.of(context)!;
    await showDialog<void>(
      context: context,
      builder: (dialogContext) => AlertDialog(
        title: Text(l10n.timerDoneTitle),
        content: Text(l10n.timerDoneBody),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(dialogContext).pop(),
            child: Text(MaterialLocalizations.of(dialogContext).okButtonLabel),
          ),
        ],
      ),
    );
  }

  String get _formattedTime {
    final minutes = _remainingSeconds ~/ 60;
    final seconds = _remainingSeconds % 60;
    return '${minutes.toString().padLeft(2, '0')}:'
        '${seconds.toString().padLeft(2, '0')}';
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final progress = _totalSeconds == 0
        ? 0.0
        : _remainingSeconds / _totalSeconds;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            Text(l10n.timerTitle, style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 16),
            SizedBox.square(
              dimension: 132,
              child: Stack(
                alignment: Alignment.center,
                children: [
                  CircularProgressIndicator(
                    value: progress,
                    strokeWidth: 9,
                    strokeCap: StrokeCap.round,
                  ),
                  Text(
                    _formattedTime,
                    style: Theme.of(context).textTheme.headlineMedium,
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
            Wrap(
              spacing: 8,
              alignment: WrapAlignment.center,
              children: [
                FilledButton.icon(
                  onPressed: _running ? null : _start,
                  icon: const Icon(Icons.play_arrow),
                  label: Text(l10n.timerStart),
                ),
                OutlinedButton.icon(
                  onPressed: _running ? _pause : null,
                  icon: const Icon(Icons.pause),
                  label: Text(l10n.timerPause),
                ),
                TextButton.icon(
                  onPressed: _reset,
                  icon: const Icon(Icons.refresh),
                  label: Text(l10n.timerReset),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
