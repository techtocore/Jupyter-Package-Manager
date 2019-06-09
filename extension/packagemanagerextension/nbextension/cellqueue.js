/**
 * Module to identify currently running cell in kernel.
 * @module cellqueue
 */

define([
    'base/js/namespace', 'base/js/events', 'notebook/js/codecell', 'jquery'
], function (
    Jupyter, events, codecell, $
) {
        var CodeCell = codecell.CodeCell;
        var current_cell;
        var last_cell;
        /**The list of cells queued for execution. */
        var cell_queue = [];
        var registered = false;

        /** Called when an execute.CodeCell event occurs. This means an execute request was sent for the current cell. */
        function cell_execute_called(event, data) {

            var cell = data.cell
            if (cell instanceof CodeCell) {
                if (cell_queue.length <= 0) {
                    events.trigger('started.currentcell', cell);
                    events.trigger('started' + cell.cell_id + 'currentcell', cell);
                }
                cell_queue.push(cell);
                current_cell = cell_queue[0];
            }
        }

        /** Called when the kernel becomes idle. This means that a cell finished executing. */
        function cell_execute_finished() {
            if (current_cell != null) {
                events.trigger('finished.currentcell', current_cell);
                events.trigger('finished' + current_cell.cell_id + 'currentcell', current_cell);
            }
            cell_queue.shift();
            current_cell = cell_queue[0]
            if (current_cell != null) {
                events.trigger('started.currentcell', current_cell);
                events.trigger('started' + current_cell.cell_id + 'currentcell', current_cell);
            }
        }
        /** @return {CodeCell} - The running cell, or null. */
        function getRunningCell() {
            return current_cell
        }

        /** @return {CodeCell} - The last run cell, or null. */
        function getLastCell() {
            return last_cell
        }

        /**
         * Called when a cell is deleted 
         * 
         * @param {event} event - The event object,
         * @param {data} data - data of the event, contains the cell
         */
        function cell_deleted(event, data) {
            var cell = data.cell;
            var i = cell_queue.indexOf(cell);
            if (i >= -1) { cell_queue.splice(i, 1); }
        }

        /** Register event listeners for detecting running cells. */
        function register() {
            if (registered) return;
            events.on('execute.CodeCell', cell_execute_called);
            events.on('kernel_idle.Kernel', cell_execute_finished);
            events.on('delete.Cell', cell_deleted);
            //TODO clear queue on execute error
            //For Debugging purposes. Highlights the currently running cell in grey colour.
            events.on('started.currentcell', function (event, cell) { cell.element.css('background-color', '#EEEEEE') });
            events.on('finished.currentcell', function (event, cell) { cell.element.css('background-color', 'white') });
        }

        return {
            'register': register,
            'getRunningCell': getRunningCell,
            'getLastCell': getLastCell
        };
    });